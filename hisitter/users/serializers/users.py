""" Users serializers."""

# Python
import logging
from collections import Counter

# Django imports
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django Rest Framework Serializers
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from hisitter.users.models import User, Babysitter, Client, Availability
from .babysitters import (
    BabysitterModelSerializer,
    AvailabilitySerializer
)

# Celery task
from hisitter.users.tasks import send_confirmation_email

# Utilities
import jwt
import time


class UserModelSerializer(serializers.ModelSerializer):
    """ User model Serializer."""
    user_bbs = BabysitterModelSerializer(read_only=True, required=False)
    
    class Meta:
        """Meta class."""
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
            'address',
            'lat',
            'long',
            'user_bbs',
        ]

        read_only_fields = (
            'reputation',
        )


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
    phone_number = serializers.CharField(validators=[phone_regex])
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    # User personal data
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    birthdate = serializers.DateField()
    address = serializers.CharField(min_length=10, max_length=255)
    genre = serializers.CharField(min_length=1, max_length=11)
    picture = serializers.ImageField(allow_empty_file=True, required=False)
    # Babysitter
    user_bbs = BabysitterModelSerializer(required=False)
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

    def validate_availability(self, value):
        """ Check if in the request only has only a unique combination
            between shift and day."""
        cnt = Counter()
        if value:
            for i in value:
                day, shift = i.values()
                mix_day_shift = str(day) + ', ' + str(shift)
                cnt[mix_day_shift] += 1
            if cnt.most_common(1)[0][1] >= 2:
                raise serializers.ValidationError(
                    f'You need set a unique combination this {cnt.most_common(1)[0]} is repeated'
                    )
        return value

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
            logging.info('This is a instance client')
            user = User.objects.create_user(**data, is_verified=False)
            logging.info(f'User created, whit pk {user.pk}')
            client = Client.objects.create(user_client=user)
        logging.info(f'User pk is already to pass {user.pk}')
        send_confirmation_email.delay(username=user.username, email=user.email )
        return user


class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer."""
    token = serializers.CharField()

    def validate_token(self, data):
        """ Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.exceptions.PyJWTError:
            raise serializers.ValidationError('Invalidad token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """ Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer
        Handle the login request data.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """ Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
