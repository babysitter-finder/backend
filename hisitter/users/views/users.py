""" Users views."""

# Django imports
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.models import Q

# Django REST Framework imports
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.generics import get_object_or_404

# Serializers
from hisitter.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
    AccountVerificationSerializer,
    BabysitterModelSerializer,
    UserLoginSerializer,
    AvailabilitySerializer
)
from hisitter.services.serializers import ServiceModelSerializer

# Permissions
from hisitter.users.permissions import IsAccountOwner

# Models
from hisitter.services.models import Service
from hisitter.users.models import User, Babysitter, Client


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ User view set.
        Handle sign up, login and account verification.
    """
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_queryset(self):
        """ Restrict the list to public only."""
        users_query = User.objects.all()
        return users_query

    def get_permissions(self):
        """Assign permissions based on actions."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """ User signup."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """ Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now find a babysitter'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def babysitter_data(self, request, *args, **kwargs):
        """Obtain de babysitter data"""
        user = self.get_object()
        try:
            user_data = UserModelSerializer(user).data
            babysitter_data = BabysitterModelSerializer(user.user_bbs).data
            user_data['babysitter_data'] = babysitter_data
            availability_data = AvailabilitySerializer(user.user_bbs.availabilities, many=True).data
            user_data['babysitter_data']['availability_data'] = availability_data
            return Response(user_data)
        except Exception:
            return Response(f'{str(user)} is not a babysitter' , status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, *kwargs)
        for user in response.data['results']:
            if user['user_bbs'] == None:
                pass
            else:
                bbs_data = Babysitter.objects.get(pk=user['user_bbs'])
                user['user_bbs'] = {
                    'cost_of_service': str(bbs_data.cost_of_service),
                    'education_degree': bbs_data.education_degree,
                }
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """ Add the service data to the response. """
        response = super(UserViewSet, self).retrieve(request, *args, *kwargs)
        user = request.user
        try:
            bbs = Babysitter.objects.get(user_bbs=user)
            services = Service.objects.filter(user_bbs=bbs, is_active=True)
        except Babysitter.DoesNotExist:
            client = get_object_or_404(Client, user_client=user)
            services = Service.objects.filter(user_client=client, is_active=True)
        data = {
            'user': response.data,
            'services': ServiceModelSerializer(services, many=True).data
        }
        response.data = data
        return response