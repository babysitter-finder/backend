""" Babysitters model."""

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils Abstract Model
from hisitter.utils.abstract_users import HisitterModel

# Models
from .users import User


class Babysitter(HisitterModel):
    """This class is to match the user and the babysitter attributes."""
    user_bbs = models.OneToOneField(
        User,
        verbose_name=_("Babysitter"),
        related_name='user_bbs',
        on_delete=models.CASCADE
    )
    education_degree = models.CharField(
        _("Education degree"),
        max_length=50,
        blank=False
    )
    about_me = models.TextField(
        _("About me"),
        blank=False
    )
    cost_of_service = models.DecimalField(
        _("Cost of service"),
        max_digits=6,
        decimal_places=2,
        blank=False
    )

    def __str__(self):
        return str(self.user_bbs)

class Availability(models.Model):
    """ This class is to create availability 
        per day for babysitting,
        requires the next fields:
        day: charfield(options)
        shift: charfield(options)
    """
    bbs = models.ForeignKey(
        "Babysitter",
        verbose_name=_("Availibility"),
        on_delete=models.CASCADE,
        related_name='availabilities',
        related_query_name='availibility'
    )
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    day = models.CharField(
        max_length=10,
        choices=DAYS,
        default='Monday'
    )
    SHIFTS = [
        ('morning', 'morning'),
        ('afternoon', 'afternoon'),
        ('evening', 'evening'),
        ('night', 'night')
    ]
    shift = models.CharField(
        max_length=10,
        choices=SHIFTS,
        default='morning'
    )

    def __str__(self):
        return str(self.bbs) + f'{self.shift}, {self.day}'