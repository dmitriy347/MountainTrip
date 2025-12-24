from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import TripMedia


@receiver(post_delete, sender=TripMedia)
def delete_trip_media_file(sender, instance, **kwargs):
    """Удаление файла изображения из файловой системы при удалении объекта TripMedia."""
    if instance.image:
        instance.image.delete(save=False)