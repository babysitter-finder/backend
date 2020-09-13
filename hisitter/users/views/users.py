""" Users views."""

# Python
import json

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
from hisitter.reviews.serializers import ReviewModelSerializer

# Permissions
from hisitter.users.permissions import IsAccountOwner, IsClient

# Models
from hisitter.services.models import Service
from hisitter.users.models import User, Babysitter, Client
from hisitter.reviews.models import Review

# Swagger
from drf_yasg.utils import swagger_auto_schema
from hisitter.utils.swagger import (
    is_authenticated_permission,
    is_account_owner_permission,
    is_client_permission
)

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
        if self.action == 'list':
            queryset = User.objects.filter(user_bbs__isnull=False)
            return queryset
        else:
            queryset = User.objects.all()
            return queryset

    def get_permissions(self):
        """Assign permissions based on actions."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated, IsClient]
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

    @action(detail=False, methods=['get'], url_path=r'verify/(?P<token>.*)')
    def verify(self, request, *args, **kwargs):
        """ Account verification."""
        serializer = AccountVerificationSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now find a babysitter'}
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            is_authenticated_permission,
            is_client_permission
            ]
    )
    @action(detail=True, methods=['get'])
    def babysitter_data(self, request, *args, **kwargs):
        """Obtain de babysitter data"""
        bbs = User.objects.get(username=kwargs['username'])
        try:
            user_data = UserModelSerializer(bbs).data
            return Response(user_data)
        except Exception:
            return Response(f'{str(bbs)} is not a babysitter' , status.HTTP_400_BAD_REQUEST)
    
    
    @swagger_auto_schema(
        manual_parameters=[
            is_authenticated_permission,
            is_account_owner_permission
            ]
    )
    def retrieve(self, request, *args, **kwargs):
        """ Add the service data to the response. """
        response = super(UserViewSet, self).retrieve(request, *args, *kwargs)
        user = request.user
        try:
            bbs = Babysitter.objects.get(user_bbs=user)
            services = Service.objects.filter(user_bbs=bbs)
            reviews = Review.objects.filter(service_origin__user_bbs=bbs)
        except Babysitter.DoesNotExist:
            client = get_object_or_404(Client, user_client=user)
            services = Service.objects.filter(user_client=client)
            reviews = None
        data = {
            'user': response.data,
            'services': ServiceModelSerializer(services, many=True).data
        }
        response.data = data
        return response
