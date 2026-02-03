from resort.models import Resort
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ResortSerializer


class ResortViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели Resort."""

    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = "slug"
