""" Users serializers."""

# Python
import logging

# Django imports
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from hisitter.users.models import User, Babysitter, Client, Availability

# Serializers
from .babysitters import (
                        BabysitterSerializer,
                        AvailabilitySerializer
                    )


class UserModelSerializer(serializers.ModelSerializer):
    """ User model Serializer."""
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'reputation',
            'birthdate',
            'picture',
            'address'
        ]

class UserSignupSerializer(serializers.Serializer):
    """ User signup Serializer.
        Handle sign up data validation and user/type user creation.
    """
    email = serializers.EmailField(
                        validators=[UniqueValidator(queryset=User.objects.all())]
                    )
    username = serializers.CharField(
                            min_length=4,
                            max_length=20,
                            validators=[UniqueValidator(queryset=User.objects.all())]
                        )
    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{10,12}',
        message='Phone number must be entered in the format: +9999999999. Up to 12 digits allowed'
    )
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    # User personal data
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    birthdate = serializers.DateField()
    address = serializers.CharField(min_length=10, max_length=255)
    genre = serializers.CharField(min_length=1, max_length=2)
    picture = serializers.ImageField(allow_empty_file=True, required=False)

    # Babysitter
    user_bbs = BabysitterSerializer(required=False)
    # Availability
    availability = AvailabilitySerializer(required=False, many=True)
    
    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data
    
    def create(self, data):
        """ Handle user and babysitter data."""
        data.pop('password_confirmation')
        try:
            availability = data.pop("availability")
            babysitter = data.pop("user_bbs")
            user = User.objects.create_user(**data, is_verified=False)
            if babysitter:
                bbs = Babysitter.objects.create(user_bbs=user, **babysitter)
                for shift in availability:
                    Availability.objects.create(bbs=bbs, **shift)
        except KeyError:
            logging.info('This is a Client instance')
            user = User.objects.create_user(**data, is_verified=False)
            client = Client.objects.create(user_client=user)
        return user