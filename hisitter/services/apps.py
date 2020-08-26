""" Services apps."""

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ServicesAppsConfig(AppConfig):
    """Services app configutarion."""
    name = 'hisitter.services'
    verbose_name = _('Services')
