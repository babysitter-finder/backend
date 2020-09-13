""" Babysitters serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from hisitter.users.models import Babysitter




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

class BabysitterFullNameSerializer(serializers.BaseSerializer):
    """ Return the first and last name for a babysitter."""
    def to_representation(self, instance):
        bbs = instance.user_bbs
        bbs_json = {
            'fullname': bbs.first_name + ' ' + bbs.last_name,
            'username': bbs.username,
            'email': bbs.email,
            'phone_number': bbs.phone_number,
            'reputation': bbs.reputation,
            'birthdate': bbs.birthdate,
            'genre': bbs.genre,
            'address': bbs.address,
            'lat': bbs.lat,
            'long': bbs.long
        }
        if bbs.picture:
            bbs_json['picture'] = bbs.picture
            return bbs_json 
        return bbs_json

class BabysitterModelSerializer(serializers.ModelSerializer):
    """This serializer is an aid to define if the user is a
        Babysitter or a regular customer."""

    availabilities = AvailabilitySerializer(read_only=True, many=True)

    class Meta:
        """ Meta class."""
        model = Babysitter
        fields =(
            'education_degree',
            'about_me',
            'cost_of_service',
            'availabilities'
        )