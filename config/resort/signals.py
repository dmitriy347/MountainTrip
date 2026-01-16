from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache_keys import CacheKeys
from .models import TripMedia, Resort, Trip


@receiver(post_delete, sender=TripMedia)
def delete_trip_media_file(sender, instance, **kwargs):
    """Удаление файла изображения из файловой системы при удалении объекта TripMedia."""
    if instance.image:
        instance.image.delete(save=False)


@receiver([post_save, post_delete], sender=Resort)
def clear_resort_cache(sender, **kwargs):
    """Очистка кэша при сохранении или удалении объекта Resort."""
    cache.delete(CacheKeys.RESORT_LIST)


@receiver([post_save, post_delete], sender=Trip)
def clear_trip_cache(sender, instance, **kwargs):
    """Очистка кэша при сохранении или удалении объекта Trip."""
    cache.delete(CacheKeys.resort_trips_counts(instance.resort_id))
