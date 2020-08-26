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
            'userbbs',
            'education_degree',
            'about_me',
            'cost_of_service'
        )

class AvailabilitySerializer(serializers.Serializer):
    """ This class define the constraints to define the availability
        of the babysitter."""
    day = serializers.ChoiceField(
        choices=[
            ('M', 'monday'),
            ('T', 'tuesday'),
            ('W', 'wednesday'),
            ('TH', 'thursday'),
            ('F', 'friday'),
            ('S', 'saturday'),
            ('SU', 'sunday')
        ]
    )
    shift = serializers.ChoiceField(
        choices=[
            ('M', 'morning'),
            ('A', 'afternoon'),
            ('E', 'evening'),
            ('N', 'night')
        ]
    )
