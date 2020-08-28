""" Reviews URLs """

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

# Views
from .views import reviews as reviews_views


router = DefaultRouter()
router.register(r'reviews/(?P<babysitter>[a-z-A-Z0-9_-]+)/babysitter', reviews_views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
