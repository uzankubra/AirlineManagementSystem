from rest_framework import serializers
from .models import Airplane, Flight, Reservation

class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

    def validate(self, data):
        if data['departure_time'] >= data['arrival_time']:
            raise serializers.ValidationError("Varış zamanı kalkış zamanından sonra olmalıdır.")
        return data

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('reservation_code', 'created_at')

    def validate(self, data):
        flight = data['flight']
        if flight.is_full():
            raise serializers.ValidationError("Uçuş dolu.")
        if flight.has_conflict():
            raise serializers.ValidationError("Uçuş çakışması tespit edildi.")
        return data