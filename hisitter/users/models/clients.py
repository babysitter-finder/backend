""" Define the Client model."""

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utils Abstract model
from hisitter.utils.abstract_users import HisitterModel

# Models
from .users import User


class Client(HisitterModel):
    """ Class which create the relation between User and client,
        this class is maked with the objective of control the children
        of each user."""
    user_client = models.OneToOneField(
        User,
        verbose_name=_("Client"),
        on_delete=models.CASCADE
    )
