from rest_framework.routers import DefaultRouter
from .views import ResortViewSet, TripViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")
router.register(r"trips", TripViewSet, basename="trip")

urlpatterns = router.urls
