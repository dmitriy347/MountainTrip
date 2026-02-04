from resort.models import Resort
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ResortSerializer
from rest_framework.filters import OrderingFilter


class ResortViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели Resort."""

    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = "slug"
    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "region"]  # Разрешенные поля для сортировки
    ordering = ["name"]  # Сортировка по умолчанию

    def get_queryset(self):
        queryset = Resort.objects.all()
        region = self.request.query_params.get("region")
        if region:
            queryset = queryset.filter(region__icontains=region)
        return queryset
