from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Airplane, Flight, Reservation
from .serializers import AirplaneSerializer, FlightSerializer, ReservationSerializer
from datetime import timedelta


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    @action(detail=True, methods=['get'])
    def flights(self, request, pk=None):
        # Belirli bir uçağın uçuşlarını listele
        airplane = self.get_object()
        flights = airplane.flights.all()
        serializer = FlightSerializer(flights, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        # Belirli bir uçuşun rezervasyonlarını listele
        flight = self.get_object()
        reservations = flight.reservations.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        flight_id = request.data.get('flight')
        flight = Flight.objects.get(id=flight_id)

        # Kapasite kontrolü
        if flight.reservations.count() >= flight.airplane.capacity:
            return Response({"error": "Uçuş dolu."}, status=status.HTTP_400_BAD_REQUEST)

        # Uçuş çakışması kontrolü
        departure_time = flight.departure_time
        arrival_time = flight.arrival_time
        conflicting_flights = Flight.objects.filter(
            airplane=flight.airplane,
            departure_time__lt=arrival_time + timedelta(hours=1),
            arrival_time__gt=departure_time - timedelta(hours=1)
        ).exclude(id=flight.id)

        if conflicting_flights.exists():
            return Response({"error": "Uçuş çakışması tespit edildi."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
