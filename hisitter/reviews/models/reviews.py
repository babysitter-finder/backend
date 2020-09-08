""" Reviews model. """

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

# Utils abstract model
from hisitter.utils.abstract_users import HisitterModel

class Review(HisitterModel):
    """ This model manage the data for do a review about a babysitter
        recieve the user_client request, and the user bbs.
    """
    service_origin = models.OneToOneField(
        "services.Service",
        verbose_name=_("Client review"),
        related_name="service_origin",
        on_delete=models.CASCADE
    )
    max_validator = MaxValueValidator(
        limit_value=5,
        message='The reputation must be written in positive integers and less than or equal to 5'
    )
    reputation = models.PositiveSmallIntegerField(
        validators=[max_validator]
    )
    review = models.TextField(
        _("Review"),
        help_text='Write how good the service was.',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return str(self.service_origin) + ', ' + f'{str(self.reputation)}'