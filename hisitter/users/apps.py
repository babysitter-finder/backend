"""Users apps"""

# Django imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppsConfig(AppConfig):
    name = "hisitter.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import hisitter.users.signals  # noqa F401
        except ImportError:
            pass
