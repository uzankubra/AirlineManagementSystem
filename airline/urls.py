from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirplaneViewSet, FlightViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'airplanes', AirplaneViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]