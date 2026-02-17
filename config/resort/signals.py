from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache_keys import CacheKeys
from .models import TripMedia, Resort, Trip
from .tasks import generate_thumbnail


@receiver(post_save, sender=TripMedia)
def create_thumbnail_on_upload(sender, instance, created, **kwargs):
    """
    Автоматически создаёт миниатюру при загрузке нового изображения.

    Args:
        sender: модель TripMedia
        instance: созданный объект TripMedia
        created: True если объект новый (не обновлённый)
        **kwargs: Дополнительные аргументы
    """
    # Запускаем задачу только для новых объектов и если у них есть изображение
    if created and instance.image:
        # Запускаем задачу асинхронно через Celery
        generate_thumbnail.delay(instance.id)
        print(f"📤 Задача генерации thumbnail отправлена в Celery для media_id={instance.id}")


@receiver(post_delete, sender=TripMedia)
def delete_trip_media_file(sender, instance, **kwargs):
    """Удаление файла изображения из файловой системы при удалении объекта TripMedia."""
    if instance.image:
        instance.image.delete(save=False)

    if instance.thumbnail:
        instance.thumbnail.delete(save=False)


@receiver([post_save, post_delete], sender=Resort)
def clear_resort_cache(sender, **kwargs):
    """Очистка кэша при сохранении или удалении объекта Resort."""
    cache.delete(CacheKeys.RESORT_LIST)


@receiver([post_save, post_delete], sender=Trip)
def clear_trip_cache(sender, instance, **kwargs):
    """Очистка кэша при сохранении или удалении объекта Trip."""
    cache.delete(CacheKeys.resort_trips_counts(instance.resort_id))
