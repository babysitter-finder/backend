""" Babysitter view set. """

# Django REST Framework imports
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Models
from hisitter.users.models import User

# Permissions
from hisitter.users.permissions import IsClient

# Serializers
from hisitter.users.serializers import UserModelSerializer


class BabysitterViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """ View set for see only the babysitters."""
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(user_bbs__isnull=False)

    def get_permissions(self):
        """Only client get acces to the data in this url."""
        permissions = [IsAuthenticated, IsClient]
        return [p() for p in permissions]

