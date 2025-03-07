from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
import uuid
from datetime import timedelta

class Airplane(models.Model):
    tail_number = models.CharField(max_length=10, unique=True)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    production_year = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tail_number} - {self.model}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')

    def __str__(self):
        return f"{self.flight_number} - {self.departure} to {self.destination}"

    def is_full(self):
        return self.reservations.count() >= self.airplane.capacity

    def has_conflict(self):
        return Flight.objects.filter(
            airplane=self.airplane,
            departure_time__lt=self.arrival_time + timedelta(hours=1),
            arrival_time__gt=self.departure_time - timedelta(hours=1)
        ).exclude(id=self.id).exists()

    def clean(self):
        overlapping_flights = Flight.objects.filter(
            airplane=self.airplane,
            departure_time__lt=self.arrival_time,
            arrival_time__gt=self.departure_time,
        ).exclude(id=self.id)

        if overlapping_flights.exists():
            raise ValidationError({
                'airplane': "Bu uçak, belirtilen zaman diliminde zaten başka bir uçuşta kullanılıyor."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(departure_time__lt=models.F('arrival_time')),
                name='check_departure_before_arrival'
            ),
            models.UniqueConstraint(
                fields=['airplane', 'departure_time', 'arrival_time'],
                name='unique_airplane_schedule'
            )
        ]


class Reservation(models.Model):
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    reservation_code = models.CharField(max_length=10, unique=True, editable=False)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reservation_code:
            self.reservation_code = self.generate_reservation_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_reservation_code():
        return uuid.uuid4().hex[:10].upper()