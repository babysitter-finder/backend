""" Reviews URLs """

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

# Views
from .views import reviews as reviews_views


router = DefaultRouter()
router.register(r'reviews/(?P<service>[0-9]+)/service', reviews_views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
