""" Serializers for service model. """

# Python
import datetime
import logging

# Django imports
from django.db.models import Q
from django.conf import settings

# Django Rest Framework Serializers
from rest_framework import serializers

# Serializers
from hisitter.reviews.serializers import ReviewModelSerializer
from hisitter.users.serializers import (
    BabysitterFullNameSerializer,
    ClientFullNameSerializer
)

# Models
from hisitter.services.models import Service
from hisitter.users.models import Availability

# Task
from hisitter.services.tasks import create_a_service_email


class ServiceModelSerializer(serializers.ModelSerializer):
    """ Service Model Serializer. """
    service_origin = ReviewModelSerializer(read_only=True)
    user_bbs = BabysitterFullNameSerializer(read_only=True)
    user_client = ClientFullNameSerializer(read_only=True)
    class Meta:
        """ Meta class. """
        model = Service
        fields = [
            'id',
            'user_client',
            'user_bbs',
            'date',
            'shift',
            'scheduled_start',
            'duration',
            'address',
            'lat',
            'long',
            'count_children',
            'special_cares',
            'is_active',
            'on_my_way',
            'arrival',
            'service_start',
            'service_end',
            'total_cost',
            'service_origin'
        ]
        read_only_fields = (
            'user_client',
            'user_bbs',
            'on_my_way',
            'arrival',
            'service_start',
            'service_end',
            'total_cost'
        )


class CreateServiceSerializer(serializers.ModelSerializer):
    """ Create Service Serializer. """
    date = serializers.DateField()
    shift = serializers.ChoiceField(
        choices=[
            ('morning', 'morning'),
            ('afternoon', 'afternoon'),
            ('evening', 'evening'),
            ('night', 'night')
        ]
    )
    scheduled_start = serializers.DateTimeField()
    count_children = serializers.IntegerField(max_value=10, min_value=1)
    special_cares = serializers.CharField(allow_blank=True)
    class Meta:
        """ Meta class. """
        model = Service
        fields = (
            'date',
            'shift',
            'scheduled_start',
            'count_children',
            'special_cares',
            'user_bbs',
            'user_client'
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
        if possible == False:
            raise serializers.ValidationError("This date and shift it's impossible.")
        services = Service.objects.filter(Q(user_bbs=data['user_bbs']) & Q(is_active=True))
        for service in services:
            if service.date == date and service.shift == shift:
                raise serializers.ValidationError('This datetime is schedule by other client')       
        return data

    def create(self, data):
        """ Create the Service. """
        client = data['user_client'].user_client
        bbs = data['user_bbs'].user_bbs
        data['address'] = client.address
        data['lat'] = client.lat
        data['long'] = client.long
        client_username = client.username
        bbs_username = bbs.username
        client_email = client.email
        bbs_email = bbs.email
        date = data['date'].strftime("%Y-%m-%w")
        shift = data['shift']
        create_a_service_email(
            client_username=client_username,
            bbs_username=bbs_username,
            client_email=client_email,
            bbs_email=bbs_email,
            date=date,
            shift=shift
        )
        service = Service.objects.create(**data, is_active=True)
        return service


class StartServiceSerializer(serializers.ModelSerializer):
    """ Start the service with the time of server. """
    service_start = serializers.DateTimeField()
    class Meta:
        """ Meta Class. """
        model = Service
        fields = ('service_start',)

    def validate_service_start(self, data):
        """ Validate if the service start in the date. """
        date = data.strftime("%A")
        date_schedule = self.context['service'].date
        date_schedule = date_schedule.strftime("%A")
        if date_schedule == date:
            return data
        else:
            raise serializers.ValidationError('The service must be start at day of schedule')


class EndServiceSerializer(serializers.ModelSerializer):
    """ Start the service with the time of server. """
    service_end = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    total_cost = serializers.DecimalField(
        max_digits=7,
        decimal_places=2    
    )
    duration = serializers.DurationField()
    class Meta:
        """ Meta Class. """
        model = Service
        fields = (
            'service_end',
            'is_active',
            'total_cost',
            'duration'
        )

    def validate_service_end(self, data):
        """ Validate if the service start in the date. """
        date = data.strftime("%A")
        service_start = self.context['service'].service_start
        if service_start:
            if service_start < data:
                return data
            else:
                raise serializers.ValidationError(
                    'The time of service end must be great than service start'
                )
        else:
            raise serializers.ValidationError(
                'The service still does not start'
            )
    
    def validate_is_active(self, data):
        """ Validate if the service is in this moment active. """
        is_active = self.context['service'].is_active
        if is_active != data:
            return data
        else:
            raise serializers.ValidationError('The service was finish before')


class OnMyWaySerializer(serializers.ModelSerializer):
    """ Serializer for babysitter on my way status. """
    on_my_way = serializers.DateTimeField()

    class Meta:
        """ Meta Class. """
        model = Service
        fields = ('on_my_way',)


class ArrivalSerializer(serializers.ModelSerializer):
    """ Serializer for babysitter arrival status. """
    arrival = serializers.DateTimeField()

    class Meta:
        """ Meta Class. """
        model = Service
        fields = ('arrival',)
