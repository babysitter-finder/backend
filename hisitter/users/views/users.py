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


class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet
            ):
    """ User view set.
        Handle sign up, login and account verification.
    """

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
        # import ipdb; ipdb.set_trace()
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
    