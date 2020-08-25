""" Babysitters serializers."""

# Django imports 
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# Models
from hisitter.users.models import Availability

class BabysitterSerializer(serializers.Serializer):
    """ This serializer is an aid to define if the user is a 
        Babysitter or a regular customer."""
    education_degree = serializers.CharField(
                                    max_length=50, 
                                    allow_blank=False
                                )
    about_me = serializers.CharField(
                            max_length=None,
                            min_length=None, 
                            allow_blank=False
                        )
    cost_of_service = serializers.DecimalField(
                                    max_digits=6, 
                                    decimal_places=2
                                )

class AvailabilitySerializer(serializers.Serializer):
    """ This class define the constraints to define the availability
        of the babysitter."""
    day = serializers.ChoiceField(
                        choices=[
                        ('M','monday'),
                        ('T','tuesday'),
                        ('W','wednesday'),
                        ('TH','thursday'),
                        ('F','friday'),
                        ('S','saturday'),
                        ('SU','sunday')
                        ]
                    )
    shift = serializers.ChoiceField(
                        choices= [
                        ('M','morning'),
                        ('A','afternoon'),
                        ('E','evening'),
                        ('N','night')
                        ]
                    )
