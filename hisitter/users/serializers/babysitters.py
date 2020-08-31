""" Babysitters serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from hisitter.users.models import Babysitter


class BabysitterModelSerializer(serializers.ModelSerializer):
    """This serializer is an aid to define if the user is a
        Babysitter or a regular customer."""
    class Meta:
        """ Meta class."""
        model = Babysitter
        fields =(
            'education_degree',
            'about_me',
            'cost_of_service'
        )

class AvailabilitySerializer(serializers.Serializer):
    """ This class define the constraints to define the availability
        of the babysitter."""
    day = serializers.ChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday')
        ]
    )
    shift = serializers.ChoiceField(
        choices=[
            ('morning', 'morning'),
            ('afternoon', 'afternoon'),
            ('evening', 'evening'),
            ('night', 'night')
        ]
    )

