"""USer permissions"""

#Django REST
from rest_framework.permissions import BasePermission

# Models
from hisitter.users.models import User


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        """Check URL username matches request user."""
        username = view.kwargs.get('username')
        if username:
            return request.user.username == username
        return True

    def has_object_permission(self, request, view, obj):
        """Check obj and user are the same"""
        return request.user == obj

class IsClient(BasePermission):
    """ Allow retrieve the babysitters only if the request user is a client."""

    def has_permission(self, request, view):
        """ Check if the user is a babysitter. """
        user = request.user
        try:
            user.user_client
            return True
        except Exception:
            return False

        