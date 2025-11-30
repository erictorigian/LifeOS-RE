from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisionViewSet, TimelineViewSet

router = DefaultRouter()
router.register(r'visions', VisionViewSet, basename='vision')
router.register(r'timelines', TimelineViewSet, basename='timeline')

urlpatterns = [
    path('', include(router.urls)),
]