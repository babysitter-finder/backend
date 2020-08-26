""" Configure for admin page."""

# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from hisitter.users.models import User, Babysitter, Availability, Client


class CustomUserAdmin(UserAdmin):
    """User model admin."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'reputation')
    list_filter = ('created_at', 'updated_at', 'deleted_at')


@admin.register(Babysitter)
class BabysitterAdmin(admin.ModelAdmin):
    """ Babysitter Admin."""
    list_display = ("user_bbs", "cost_of_service")
    search_fields = ("user_bbs__username", "user_bbs__email", "user_bbs__reputation")
    list_filter = ("cost_of_service",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Client Admin."""
    list_display = ('user_client',)
    search_fields = ('user_client__username', 'user_client__email')


@admin.register(Availability)
class Availability(admin.ModelAdmin):
    """ Availability Admin."""
    list_display = ('bbs', 'day', 'shift')


admin.site.register(User, CustomUserAdmin)
