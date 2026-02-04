from rest_framework.routers import DefaultRouter
from .views import ResortViewSet, TripViewSet, TripMediaViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"media", TripMediaViewSet, basename="tripmedia")

urlpatterns = router.urls
