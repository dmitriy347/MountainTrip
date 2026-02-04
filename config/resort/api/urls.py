from rest_framework.routers import DefaultRouter
from .views import ResortViewSet, TripViewSet, TripMediaViewSet, UserViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"media", TripMediaViewSet, basename="tripmedia")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls
