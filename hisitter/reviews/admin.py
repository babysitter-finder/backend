""" Admin for control Reviews model. """

# Django imports
from django.contrib import admin

# Models
from hisitter.reviews.models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Admin. """
    list_display = ('service_origin', 'reputation')
    list_filter = ('created_at', 'updated_at', 'deleted_at')
