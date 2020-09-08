""" Reviews permissions."""

# Python
import logging

# Django Rest Framework 
from rest_framework.permissions import BasePermission


class IsServiceOwner(BasePermission):
    """ This permission allow determine if the user
        is a client, if not permission is denied.
    """
    def has_permission(self, request, view):
        """ Manage the permission if the user is a client. """
        try:
            user = request.user.user_client
            if user == view.service.user_client:
                return True
            else:
                return False
        except Exception as error:
            logging.info(f'We have a problem that Exception raise {error}')
