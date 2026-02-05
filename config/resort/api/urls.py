from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ResortViewSet, TripViewSet, TripMediaViewSet, UserViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"media", TripMediaViewSet, basename="tripmedia")
router.register(r"users", UserViewSet, basename="user")


urlpatterns = [
    # JWT эндпоинты
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
