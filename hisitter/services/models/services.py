""" Services model module. """

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

# Utils Abstract model
from hisitter.utils.abstract_users import HisitterModel

class Service(HisitterModel):
    """ This model hast the main activity in the application
        recieving the user-client, and the user-bbs, on the
        service of attention to the child or children.
    """
    user_client = models.ForeignKey(
        "users.Client",
        verbose_name=_("Customer"),
        related_name='client_service',
        on_delete=models.CASCADE
    )
    user_bbs = models.ForeignKey(
        "users.Babysitter",
        verbose_name=_("Babysitter"),
        related_name='bbs_service',
        on_delete=models.CASCADE
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False,
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
    duration = models.DurationField(
        blank=True,
        null=True
    )
    address = models.CharField(
        _("Address"),
        max_length=255
    )
    lat = models.DecimalField(
        _("Latitude"),
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True
    )
    long =  models.DecimalField(
        _("Latitude"),
        max_digits=10,
        decimal_places=6,
        blank=True,
        null=True
    )    
    max_validator = MaxValueValidator(
        limit_value=10,
        message='The maximum number of children per babysitter must be 10'
    )
    count_children = models.PositiveSmallIntegerField(validators=[max_validator])
    special_cares = models.CharField(
        _("Special Cares"),
        max_length=255,
        help_text='Write the special cares to consider for each child',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        _("Service Active"),
        default=True
    )
    scheduled_start = models.DateTimeField(
        _("Scheduled service start time"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        help_text="The scheduled start time with timezone"
    )
    on_my_way = models.DateTimeField(
        _("Babysitter on the way"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    service_start = models.DateTimeField(
        _("Datetime service starts"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    service_end = models.DateTimeField(
        _("Datetime service ends"),
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    total_cost = models.DecimalField(
        _("Total service cost"),
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    def __str__(self):
        return  'id ' + str(self.id) + ', ' + str(self.user_client) + f'{str(self.user_bbs)}, {str(self.date)}'