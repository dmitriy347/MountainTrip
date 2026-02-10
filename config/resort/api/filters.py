import django_filters

from resort.models import Resort, Trip


class ResortFilter(django_filters.FilterSet):
    """Фильтр для модели Resort."""

    # Поиск по региону (частичное совпадение, без учета регистра)
    region = django_filters.CharFilter(
        field_name="region",
        lookup_expr="icontains",
        label="Регион (частичное совпадение)",
    )

    # Поиск по названию курорта (частичное совпадение, без учета регистра)
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Название курорта (частичное совпадение)",
    )

    class Meta:
        model = Resort
        fields = ["region", "name"]


class TripFilter(django_filters.FilterSet):
    """Фильтр для модели Trip."""

    # Фильтр по публичности поездки
    is_public = django_filters.BooleanFilter(
        field_name="is_public", label="Публичная поездка"
    )

    # Фильтр по курорту (ID)
    resort_id = django_filters.NumberFilter(field_name="resort__id", label="ID курорта")

    # Фильтр по региону курорта (частичное совпадение, без учета регистра)
    resort_region = django_filters.CharFilter(
        field_name="resort__region",
        lookup_expr="icontains",
        label="Регион курорта (частичное совпадение)",
    )

    # Фильтр по диапазону дат
    start_date_from = django_filters.DateFilter(
        field_name="start_date", lookup_expr="gte", label="Дата начала поездки (от)"
    )

    start_date_to = django_filters.DateFilter(
        field_name="start_date", lookup_expr="lte", label="Дата начала поездки (до)"
    )

    end_date_from = django_filters.DateFilter(
        field_name="end_date", lookup_expr="gte", label="Дата окончания поездки (от)"
    )

    end_date_to = django_filters.DateFilter(
        field_name="end_date", lookup_expr="lte", label="Дата окончания поездки (до)"
    )

    class Meta:
        model = Trip
        fields = [
            "is_public",
            "resort_id",
            "resort_region",
            "start_date_from",
            "start_date_to",
            "end_date_from",
            "end_date_to",
        ]
