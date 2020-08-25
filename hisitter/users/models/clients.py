""" Define the Client model."""

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Models
from .users import User

# Utils Abstract model
from hisitter.utils.abstract_users import HisitterModel


class Client(HisitterModel):
    """ Class which create the relation between User and client,
        this class is maked with the objective of control the children
        of each user."""

    user_client =  models.OneToOneField(User, 
                            verbose_name=_("Client"), 
                            on_delete=models.CASCADE
                        )
class Child(models.Model):
    """ Class to define the child or children per Client. """
    client = models.ForeignKey("Client",
            verbose_name=_("Client"), 
            on_delete=models.CASCADE,
            related_name='children',
            related_query_name='child'
        )
    birthdate = models.DateField('birthdate',
                        blank=False
                    )
    GENRES = [
        ('M', 'male'),
        ('F', 'female'),
        ('SE', 'Unspecified')
    ]
    genre = models.CharField(
                    max_length=2,
                    choices=GENRES,
                    default='SE'
                )
    features_medical = models.TextField(_("features medical"),
                    blank=False
                )                      