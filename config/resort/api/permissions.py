from rest_framework import permissions


class IsOwnerReadOnly(permissions.BasePermission):
    """
    Кастомный permission:
    - Читать могут все (GET)
    - Изменять/удалять может только владелец (POST/PUT/PATCH/DELETE)
    """

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа к объекту."""
        # Если запрос безопасный (GET, HEAD, OPTIONS), права доступа есть у всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Изменение разрешено только владельцу
        # obj.user - для Trip
        # obj.trip.user - для TripMedia
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "trip"):
            return obj.trip.user == request.user
        return False
