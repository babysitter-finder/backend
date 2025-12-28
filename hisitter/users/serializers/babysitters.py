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
            bbs_json['picture'] = bbs.picture.url
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


class BabysitterPublicSerializer(serializers.BaseSerializer):
    """Public babysitter profile for clients.

    Limited fields - excludes sensitive data like email, phone, address.
    """
    def to_representation(self, instance):
        # instance is the User object
        bbs_data = None
        if hasattr(instance, 'user_bbs') and instance.user_bbs:
            bbs = instance.user_bbs
            bbs_data = {
                'education_degree': bbs.education_degree,
                'about_me': bbs.about_me,
                'cost_of_service': str(bbs.cost_of_service),
                'availabilities': [
                    {'day': a.day, 'shift': a.shift}
                    for a in bbs.availabilities.all()
                ]
            }

        data = {
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'fullname': f"{instance.first_name} {instance.last_name}",
            'reputation': str(instance.reputation),
            'genre': instance.genre,
            'user_bbs': bbs_data
        }

        if instance.picture:
            data['picture'] = instance.picture.url
        else:
            data['picture'] = None

        return data