

class OwnerQuerySetMixin:
    """Ограничивает видимость объектов только владельцем."""
    owner_field = 'user'

    def get_queryset(self):
        """Фильтрация queryset по текущему пользователю."""
        qs = super().get_queryset()
        filter_kwargs = {self.owner_field: self.request.user}
        return qs.filter(**filter_kwargs)