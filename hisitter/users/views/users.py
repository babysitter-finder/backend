""" Users views."""

# Django REST Framework imports
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

# Serializers
from hisitter.users.serializers import (
    UserModelSerializer,
    UserSignupSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)

# Models
from hisitter.users.models import User


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """ User view set.
        Handle sign up, login and account verification.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permission(self):
        """Assign permissions based on actions."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action == ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated]
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

    @action(detail=True, methods=['put', 'patch'])
    def user_data(self, request, *args, **kwargs):
        """Update user data, can be partial update or total"""
        user = self.get_object()
        partial = request.method == 'PATCH'
        serializer = UserModelSerializer(
            user,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
