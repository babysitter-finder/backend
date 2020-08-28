""" Admin for control Service models. """

# Django imports
from django.contrib import admin

# Models
from hisitter.services.models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """ Service Admin. """
    list_display = ('user_client', 'user_bbs', 'date')
    search_fields = ('date', 'user_client__username', 'user_bbs__pk')
    list_filter = ('created_at', 'updated_at', 'deleted_at', 'is_active')
