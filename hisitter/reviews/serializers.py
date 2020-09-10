""" Review Serializers. """

# Django imports
from django.db.models import Avg

# Django Rest Framework Serializers
from rest_framework import serializers

# Models
from hisitter.reviews.models import Review

class CreateReviewModelSerializer(serializers.ModelSerializer):
    """ Create Review Serializer. """

    class Meta:
        """ Meta class. """
        model = Review
        fields = (
            'reputation',
            'review',
        )
        read_only_fields = (
            'service_origin',
        )

    def validate(self, data):
        """ Validate if the service ends in the momento of the review."""
        service = self.context['service']
        if service.is_active:
            raise serializers.ValidationError('You need to finish the Service after write a review.')
        data['service'] = service
        return data
        
    def create(self, data):
        """ Create the review. """
        user_bbs = data['service'].user_bbs.user_bbs
        review = Review.objects.create(
            service_origin=data['service'],
            review=data['review'],
            reputation=data['reputation']
        )
        reputation_avg = Review.objects.filter(
            service_origin__user_bbs__user_bbs=user_bbs
        ).aggregate(Avg('reputation'))
        user_bbs.reputation = reputation_avg['reputation__avg']
        user_bbs.save()
        return review

class ReviewModelSerializer(serializers.ModelSerializer):
    """ Create the review model serializer to retrieve the data in the
        bbs view.
    """
    class Meta:
        """ Meta class."""
        model = Review
        fields = (
            'id',
            'reputation',
            'review'
        )
    