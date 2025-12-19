from django.db import models

class Resort(models.Model):
    """Модель справочник, к которому привязаны поездки."""
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name