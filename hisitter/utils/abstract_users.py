""" Configuration of initial user fields by default in each model."""

#Django imports
from django.db import models

class HisitterModel(models.Model):
    """ HisitterModel has the default fields configuration that
        contain the data about de dates that each class will be inherit,
        those are:
            * created_at(Datetime): store the dateimte the object was created.
            * updated_at(Datatime): store the last modification of the object.
            * deleted_at(Datetime): store the date at the object will be hidden
                    for the app.
    """
    created_at = models.DateTimeField('created at', 
                        auto_now_add=True,
                        help_text='Date time on which the object was created.'
                    )
    updated_at = models.DateTimeField('updated at',
                        auto_now=True,
                        help_text='Date time on which the object was modified'
                    )
    deleted_at = models.DateTimeField('deleted at',
                        editable=True,
                        blank=True,
                        null=True
                    )

    class Meta:
        """Meta options."""
        abstract = True
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-updated_at']