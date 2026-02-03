from rest_framework.routers import DefaultRouter
from .views import ResortViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")

urlpatterns = router.urls
