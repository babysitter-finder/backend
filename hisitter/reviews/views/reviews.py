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

# Models
from hisitter.users.models import Babysitter, User, Client
from hisitter.services.models import Service
from hisitter.reviews.models import Review

class ReviewViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """ Review view set. """

    def dispatch(self, request, *args, **kwargs):
        """ Obtain the babysitter as url parameter, to return 
            all the reviews about that babysitter. """
        bbs_username = kwargs['babysitter']
        self.babysitter = get_object_or_404(Babysitter, username=bbs_username)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """ Return service review data. """
        
    