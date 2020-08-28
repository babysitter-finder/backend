""" Service views."""

# Django imports
from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor
from django.db.models import Q

# Django REST Framework imports
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404

# Serializers
from hisitter.services.serializers import ServiceModelSerializer, CreateServiceSerializer

# Models
from hisitter.users.models import Babysitter, Client
from hisitter.services.models import Service

# Permissions
from hisitter.services.permissions import IsServiceOwner, IsUserClient


class ServiceViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """ Service View Set.
        Handle create, list, update and retrieve services.
    """

    def get_queryset(self):
        """ Return services data. """
        if self.action in ('list', 'retrieve'):
            return Service.objects.filter(
                Q(user_client__user_client__username=self.request.user.username) |
                Q(user_bbs__user_bbs__username=self.request.user.username)
            )
     
    def get_permissions(self):
        """ Assign permissions bassed on actions."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update','start', 'finish']:
            permissions.append(IsServiceOwner)
        return [p() for p in permissions]

    @action(detail=True, methods=['patch'])
    def start(self, request, *args, **kwargs):
        """ Start the service. """
        import ipdb; ipdb.set_trace()

class ServiceCreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """ Create the service with babysitting information.
        This information will be passed in the url.
    """
    serializer_class = CreateServiceSerializer

    def dispatch(self, request, *args, **kwargs):
        """ Verify that Babysitter exists. """
        babysitter = kwargs['babysitter']
        self.babysitter = get_object_or_404(Babysitter, user_bbs__username=babysitter)
        return super(ServiceCreateViewSet, self).dispatch(request, *args, **kwargs)
    def get_permissions(self):
        """ Validate if the request user is client, a babysitter
            can't create a service.
        """
        permissions = [IsAuthenticated, IsUserClient]
        return [p() for p in permissions]

    def get_queryset(self, *args, **kwargs):
        """ Determine the queryset of the viewset ServiceCreate."""
        return Babysitter.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        """ Add user and babysitter to serializer context. """
        context = super(ServiceCreateViewSet, self).get_serializer_context()
        context['babysitter'] = self.babysitter

    def create(self, request, *args, **kwargs):
        """ Create the service with information of babysitter."""
        user = request.user.pk
        user_client = Client.objects.get(user_client=user)
        babysitter = self.babysitter.pk
        request.data['user_client'] = user_client.pk
        request.data['user_bbs'] = babysitter
        return super(ServiceCreateViewSet, self).create(request, *args, **kwargs)
