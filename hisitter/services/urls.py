""" Services URLs """

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import services as service_views

# Django imports
from django.urls import path, include

router = DefaultRouter()
router.register(r'services', service_views.ServiceViewSet, basename='services')
router.register(r'services', service_views.ServiceCreateViewSet, basename='services-creation')

urlpatterns = [
    path('', include(router.urls)),
]
