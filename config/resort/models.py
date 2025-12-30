from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from slugify import slugify


class Resort(models.Model):
    """Модель справочник, к которому привязаны поездки."""
    name = models.CharField(max_length=150, verbose_name='Название курорта')
    region = models.CharField(max_length=100, verbose_name='Регион')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Динамический URL для курорта."""
        return reverse('resort_detail', kwargs={'resort_slug': self.slug})

    def save(self, *args, **kwargs):
        """Автоматическое создание slug из названия курорта при сохранении."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Курорт'
        verbose_name_plural = 'Курорты'


class Trip(models.Model):
    """Модель поездка пользователя."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips', verbose_name='Пользователь')
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='trips', verbose_name='Курорт')
    start_date = models.DateField(verbose_name='Дата начала поездки')
    end_date = models.DateField(verbose_name='Дата окончания поездки')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    is_public = models.BooleanField(default=False, verbose_name='Публичная поездка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.user.username} - {self.resort.name}"

    def clean(self):
        """Валидация: дата начала не может быть позже даты окончания."""
        if self.start_date > self.end_date:
            raise ValidationError('Дата начала поездки не может быть позже даты окончания.')

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Поездку'
        verbose_name_plural = 'Поездки'

    def get_absolute_url(self):
        """Динамический URL для поездки."""
        return reverse('trip_detail', kwargs={'trip_id': self.id})


class TripMedia(models.Model):
    """Модель для хранения медиафайлов, связанных с поездкой."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='media', verbose_name='Поездка')
    image = models.ImageField(upload_to='trip_photos/', verbose_name='Фотография')     # Для работы с ImageField требуется Pillow
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    def __str__(self):
        return f"Media for trip {self.trip.id}"

    def get_absolute_url(self):
        """Динамический URL для медиафайла."""
        return self.trip.get_absolute_url()

    class Meta:
        verbose_name = 'Фотографию поездки'
        verbose_name_plural = 'Фотографии поездок'