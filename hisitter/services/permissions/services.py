""" Service permissions."""

# Django Rest Framework 
from rest_framework.permissions import BasePermission

# Models
from hisitter.users.models import User, Babysitter, Client

class IsUserClient(BasePermission):
    """ This permission allow determine if the user
        is a client, if not permission is denied.
    """
    def has_permission(self, request, view):
        """ Manage the permission if the user is a client. """
        user = request.user.username
        try:
            client = Client.objects.get(user_client__username=user)
            return True
        except Client.DoesNotExist:
            return False
