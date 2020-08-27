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
            ('MONDAY', 'monday'),
            ('TUESDAY', 'tuesday'),
            ('WEDNESDAY', 'wednesday'),
            ('THURSDAY', 'thursday'),
            ('FRIDAY', 'friday'),
            ('SATURDAY', 'saturday'),
            ('SUNDAY', 'sunday')
        ]
    )
    shift = serializers.ChoiceField(
        choices=[
            ('MORNING', 'morning'),
            ('AFTERNOON', 'afternoon'),
            ('EVENING', 'evening'),
            ('NIGHT', 'night')
        ]
    )
