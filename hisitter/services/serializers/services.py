""" Serializers for service model. """

# Python
import datetime
import logging

# Django imports
from django.db.models import Q

# Django Rest Framework Serializers
from rest_framework import serializers

# Models
from hisitter.services.models import Service
from hisitter.users.models import Availability

class ServiceModelSerializer(serializers.ModelSerializer):
    """ Service Model Serializer. """
    class Meta:
        """ Meta class. """
        model = Service
        fields = [
            'id',
            'user_client',
            'user_bbs',
            'date',
            'duration',
            'address',
            'count_children',
            'special_cares',
            'is_active'
        ]
        read_only_fields = (
            'user_client',
            'user_bbs'
        )

class CreateServiceSerializer(serializers.ModelSerializer):
    """ Create Service Serializer. """


    class Meta:
        """ Mata class. """
        model = Service
        exclude = (
            'is_active',
            'duration',
            'total_cost',
            'service_end',
            'service_start',
        )

    def validate(self, data):
        """ Validate if the date it's a day in the availability registers
            of the Babysitter.
        """
        availabilities = Availability.objects.filter(bbs=data['user_bbs'])
        date = data['date']
        weekday = date.strftime("%A")
        shift = data['shift']
        possible = False
        for availability in availabilities:
            if availability.day == weekday and shift == availability.shift:
                logging.info('This date and shift is available')
                possible = True
        if possible:
            raise serializers.ValidationError("This date it's impossible.")        
                
        services = Service.objects.filter(Q(user_bbs=data['user_bbs']) & Q(is_active=True))
        for service in services:
            if service.date == date and service.shift == shift:
                raise serializers.ValidationError('This datetime is schedule by other client')
        return data

    def create(self, data):
        """ Create the Service. """
        service = Service.objects.create(**data, is_active=True)
        return service