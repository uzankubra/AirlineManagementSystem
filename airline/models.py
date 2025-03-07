from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
import uuid
from datetime import timedelta

class Airplane(models.Model):
    tail_number = models.CharField(max_length=10, unique=True)  # Uçak kuyruk numarası
    model = models.CharField(max_length=50)  # Uçak modeli
    capacity = models.IntegerField()  # Yolcu kapasitesi
    production_year = models.IntegerField()  # Üretim yılı
    status = models.BooleanField(default=True)  # Uçak durumu (aktif/pasif)

    def __str__(self):
        return f"{self.tail_number} - {self.model}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)  # Uçuş numarası
    departure = models.CharField(max_length=100)  # Kalkış yeri
    destination = models.CharField(max_length=100)  # Varış yeri
    departure_time = models.DateTimeField()  # Kalkış zamanı
    arrival_time = models.DateTimeField()  # Varış zamanı
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')  # Uçak ilişkisi

    def __str__(self):
        return f"{self.flight_number} - {self.departure} to {self.destination}"

    def is_full(self):
        # Uçuşun dolu olup olmadığını kontrol et
        return self.reservations.count() >= self.airplane.capacity

    def has_conflict(self):
        # Aynı uçağın başka bir uçuşuyla çakışma kontrolü
        return Flight.objects.filter(
            airplane=self.airplane,
            departure_time__lt=self.arrival_time + timedelta(hours=1),
            arrival_time__gt=self.departure_time - timedelta(hours=1)
        ).exclude(id=self.id).exists()

    def clean(self):
        """
        Aynı uçağın aynı zaman diliminde birden fazla uçuşta kullanılamayacağını kontrol eder.
        """
        # Aynı uçağın aynı zaman diliminde başka bir uçuşu var mı kontrol et
        overlapping_flights = Flight.objects.filter(
            airplane=self.airplane,
            departure_time__lt=self.arrival_time,  # Mevcut uçuşun kalkış zamanından önce başlayan uçuşlar
            arrival_time__gt=self.departure_time,  # Mevcut uçuşun varış zamanından sonra biten uçuşlar
        ).exclude(id=self.id)  # Mevcut uçuşu hariç tut (güncelleme durumu için)

        if overlapping_flights.exists():
            raise ValidationError({
                'airplane': "Bu uçak, belirtilen zaman diliminde zaten başka bir uçuşta kullanılıyor."
            })

    def save(self, *args, **kwargs):
        """
        Model kaydedilmeden önce doğrulama yapar.
        """
        self.full_clean()  # clean metodunu çağırarak doğrulama yap
        super().save(*args, **kwargs)

    class Meta:
        """
        Veritabanı seviyesinde kısıtlamalar ekler.
        """
        constraints = [
            # Kalkış zamanının varış zamanından önce olmasını sağlar
            models.CheckConstraint(
                check=Q(departure_time__lt=models.F('arrival_time')),
                name='check_departure_before_arrival'
            ),
            # Aynı uçağın aynı zaman diliminde birden fazla uçuşta kullanılamayacağını garanti eder
            models.UniqueConstraint(
                fields=['airplane', 'departure_time', 'arrival_time'],
                name='unique_airplane_schedule'
            )
        ]


class Reservation(models.Model):
    passenger_name = models.CharField(max_length=100)  # Yolcu adı
    passenger_email = models.EmailField()  # Yolcu e-posta
    reservation_code = models.CharField(max_length=10, unique=True, editable=False)  # Rezervasyon kodu
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations')  # Uçuş ilişkisi
    status = models.BooleanField(default=True)  # Rezervasyon durumu
    created_at = models.DateTimeField(auto_now_add=True)  # Rezervasyon tarihi

    def __str__(self):
        return f"{self.reservation_code} - {self.passenger_name}"

    def save(self, *args, **kwargs):
        # Rezervasyon kodu otomatik oluşturulur
        if not self.reservation_code:
            self.reservation_code = self.generate_reservation_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_reservation_code():
        # Benzersiz bir rezervasyon kodu oluştur
        return uuid.uuid4().hex[:10].upper()