""" Service views."""

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

# Serializers
from hisitter.services.serializers import (
    ServiceModelSerializer,
    CreateServiceSerializer,
    StartServiceSerializer,
    EndServiceSerializer
)

# Models
from hisitter.users.models import Babysitter, Client
from hisitter.services.models import Service

# Permissions
from hisitter.services.permissions import IsUserClient

# Utils
from hisitter.utils.functions_utils import time_cost_treatment

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        return [p() for p in permissions]
    
    def get_serializer_class(self):
        """ Return seralizer based on action."""
        if self.action == 'start':
            return StartServiceSerializer
        if self.action == 'end':
            return EndServiceSerializer
        else:
            return ServiceModelSerializer

    @action(detail=True, methods=['patch'])
    def start(self, request, *args, **kwargs):
        """ Start the service. """
        self.service = Service.objects.get(pk=kwargs['pk'])
        date = datetime.datetime.now()
        if (request.user.user_client == 
            self.service.user_client) or (
                request.user.user_client == self.service.user_bbs):
            logging.info('Permiso concedido')
        else:
            error = {"You don't have permissions to acces in this service"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        serializer = StartServiceSerializer(
            self.service,
            data={'service_start': date},
            partial=True,
            context={'service': self.service}
        )
        serializer.is_valid(raise_exception=True)
        service = serializer.save()
        data = ServiceModelSerializer(service).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def end(self, request, *args, **kwargs):
        """ Start the service. """
        self.service = Service.objects.get(pk=kwargs['pk'])
        
        service_start = self.service.service_start
        if not service_start:
            error = {"This services doesn't start still"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        service_end = datetime.datetime.now(timezone.utc)
        self.babysitter = self.service.user_bbs
        cost_per_hour = self.babysitter.cost_of_service
        if (request.user.user_client == 
            self.service.user_client) or (
                request.user.user_client == self.service.user_bbs):
            logging.info('Permiso concedido')
        else:
            error = {"You don't have permissions to acces in this service"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        total_cost = time_cost_treatment(
            service_start,
            service_end,
            cost_per_hour
        )
        date = datetime.datetime.now()
        serializer = EndServiceSerializer(
            self.service,
            data={
                'service_end': date,
                'total_cost': total_cost,
                'is_active': False
            },
            partial=True,
            context={'service': self.service}
        )
        serializer.is_valid(raise_exception=True)
        service = serializer.save()
        data = ServiceModelSerializer(service).data
        return Response(data, status=status.HTTP_200_OK)


class ServiceCreateViewSet(
    viewsets.GenericViewSet
):
    """ Create the service with babysitting information.
        This information will be passed in the url.
    """

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

    def get_serializer_class(self):
        """ Return the serializer class for create a Service."""
        if self.action == 'create_service':
            return CreateServiceSerializer

    operation_description= "Create a service with the information of the babysitter, and details of service."
    service_created_response = openapi.Response("Retrieve the partial detail of Serviece", ServiceModelSerializer)       
    @swagger_auto_schema(
        operation_decription=operation_description,
        responses={201: service_created_response},
        request_body=CreateServiceSerializer
    )
    @action(detail=False, methods=['post'], url_path=r'create/(?P<babysitter>[a-z-A-Z0-9_-]+)')
    def create_service(self, request, *args, **kwargs):
        """ Create the service with information of babysitter."""
        user = request.user.pk
        user_client = Client.objects.get(user_client=user)
        babysitter = self.babysitter.pk
        request.data['user_client'] = user_client.pk
        request.data['user_bbs'] = babysitter
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context=self.get_serializer_context(),
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        service = serializer.save()
        data = ServiceModelSerializer(service).data
        return Response(data, status=status.HTTP_201_CREATED)
