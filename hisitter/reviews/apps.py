"""Users apps"""

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReviewsAppsConfig(AppConfig):
    name = "hisitter.reviews"
    verbose_name = _("Reviews")
