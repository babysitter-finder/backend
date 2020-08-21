""" Users serializers."""

# Django imports
from django.conf import settings
from django.contrib.auth import password_validator, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from hisitter.users.models import User, Babysitter, Client

class UserModelSerializer(serializers.ModelSerializer):
    """ User model Serializer."""
    class Meta:
        model = User
        fields = [
            'username',
            'fist_name',
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
    birthdate = serializers.DateTimeField()
    address = serializers.CharField(min_length=10, max_length=255)
    genre = serializers.CharField(min_length=1, max_length=2)
    picture = serializers.ImageField(allow_empty_file=True)
    #Babysitter data
    education_degree = serializers.CharField(min_length=10, max_length=50, allow)