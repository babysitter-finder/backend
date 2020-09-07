""" Reviews view."""

# Ptyhon
import datetime
from datetime import timezone
import logging

# Django imports
from django.db.models import Q

# Django REST Framework imports
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

# Permissions
from hisitter.services.permissions import IsUserClient
from hisitter.reviews.permissions import IsServiceOwner

# Models
from hisitter.users.models import Babysitter, User, Client
from hisitter.services.models import Service
from hisitter.reviews.models import Review

# Serializers
from hisitter.reviews.serializers import CreateReviewModelSerializer, ReviewModelSerializer

class ReviewViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """ Review view set. """

    serializer_class = CreateReviewModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """ Obtain the babysitter as url parameter, to return 
            all the reviews about that babysitter. """
        service = kwargs['service']
        self.service = get_object_or_404(Service, id=service)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """ Return service review data. """
        babysitter = Babysitter.objects.all()

    def get_permissions(self):
        """ Validate if the user in the request is owner of the service.
            else, denied the permission.
        """
        permissions = [IsAuthenticated, IsUserClient, IsServiceOwner]
        return [p() for p in permissions]

    def get_serializer_context(self, *args, **kwargs):
        """ Add the service in the serializer for create the review."""
        context = super(ReviewViewSet, self).get_serializer_context()
        context['service'] = self.service
        return context
