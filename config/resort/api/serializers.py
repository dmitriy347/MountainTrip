from rest_framework import serializers
from resort.models import Resort


class ResortSerializer(serializers.ModelSerializer):
    """Serializer для модели Resort."""

    class Meta:
        model = Resort
        fields = ['id', 'name', 'slug', 'region', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']