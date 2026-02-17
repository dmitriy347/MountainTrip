import os
from celery import shared_task
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_thumbnail(self, media_id):
    """
    Генерация миниатюры (thumbnail) для загруженного изображения.

    Args:
        media_id: ID объекта TripMedia
    """
    # Импортируем модель внутри функции, т.к. Celery загружается до Django
    from resort.models import TripMedia

    try:
        # Получаем объект медиафайла
        media = TripMedia.objects.get(id=media_id)

        # Если миниатюра уже существует, пропускаем
        if media.thumbnail:
            print(f"⚠️ Thumbnail уже существует для media_id={media_id}")
            return f"Thumbnail already exists for media_id={media_id}"

        # Открываем исходное изображение
        image_path = media.image.path
        img = Image.open(image_path)

        # Конвертируем в RGB, если изображение в RGBA (PNG с прозрачностью)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        # Создаём миниатюру (максимум 300x300px, с сохранением пропорций)
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)

        # Сохраняем в BytesIO
        thumb_io = BytesIO()
        img.save(thumb_io, format="JPEG", quality=85)
        thumb_io.seek(0)

        # Генерируем имя файла для миниатюры
        original_name = os.path.basename(media.image.name)
        thumb_name = f"thumb_{original_name}"

        # Сохраняем миниатюру в модель
        media.thumbnail.save(thumb_name, ContentFile(thumb_io.read()), save=True)

        print(f"✅ Thumbnail создан для media_id={media_id}: {thumb_name}")

        return f"Thumbnail created: {thumb_name}"

    except TripMedia.DoesNotExist:
        print(f"❌ TripMedia с id={media_id} не найден")
        return f"Error: TripMedia {media_id} not found"

    except Exception as exc:
        raise self.retry(exc=exc)
