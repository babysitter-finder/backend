""" Users views."""

# Python
import json

# Django imports
from django.db.models import Q
from django.shortcuts import render, redirect

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
    BabysitterPublicSerializer,
    UserLoginSerializer,
    AvailabilitySerializer
)

# Permissions
from hisitter.users.permissions import IsAccountOwner, IsClient

# Models
from hisitter.users.models import User, Babysitter, Client

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
        elif self.action in ['list', 'babysitter_data']:
            permissions = [IsAuthenticated]
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
        # return Response(data, status=status.HTTP_200_OK)
        return redirect('https://frontend-kappa-eight.vercel.app/')

    @swagger_auto_schema(
        manual_parameters=[is_authenticated_permission]
    )
    @action(detail=True, methods=['get'])
    def babysitter_data(self, request, *args, **kwargs):
        """Obtain babysitter data.

        Returns full data if requester is the owner, otherwise returns public data only.
        """
        try:
            bbs_user = User.objects.get(username=kwargs['username'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not hasattr(bbs_user, 'user_bbs') or not bbs_user.user_bbs:
            return Response({'error': f'{bbs_user.username} is not a babysitter'}, status=status.HTTP_400_BAD_REQUEST)

        # Owner gets full data, others get public data only
        if request.user.username == kwargs['username']:
            user_data = UserModelSerializer(bbs_user).data
        else:
            user_data = BabysitterPublicSerializer(bbs_user).data

        return Response(user_data)
    
    
    @swagger_auto_schema(
        manual_parameters=[
            is_authenticated_permission,
            is_account_owner_permission
            ]
    )
    def retrieve(self, request, *args, **kwargs):
        """ Return user data. """
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
