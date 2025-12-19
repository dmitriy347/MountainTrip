from django.contrib.auth.models import User
from django.db import models


class Resort(models.Model):
    """Модель справочник, к которому привязаны поездки."""
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    """Модель поездка пользователя."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='trips')
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.resort.name}"


class TripMedia(models.Model):
    """Модель для хранения медиафайлов, связанных с поездкой."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='media')
    image = models.ImageField(upload_to='trip_photos/')     # Для работы с ImageField требуется Pillow
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for trip {self.trip.id}"