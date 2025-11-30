from rest_framework import viewsets
from .models import Vision, Timeline
from .serializers import VisionSerializer, TimelineSerializer


class VisionViewSet(viewsets.ModelViewSet):
    queryset = Vision.objects.all().order_by('-created_at')
    serializer_class = VisionSerializer


class TimelineViewSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all().order_by('-created_at')
    serializer_class = TimelineSerializer