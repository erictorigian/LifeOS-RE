from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.auth_utils import get_user_id_from_request
from .models import Vision, Timeline
from .serializers import VisionSerializer, TimelineSerializer


class VisionViewSet(viewsets.ModelViewSet):
    serializer_class = VisionSerializer
    
    def get_queryset(self):
        """Filter visions by user_id from authenticated user"""
        user_id = get_user_id_from_request(self.request)
        return Vision.objects.filter(user_id=user_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Automatically set user_id when creating a vision"""
        user_id = get_user_id_from_request(self.request)
        serializer.save(user_id=user_id)
    
    def perform_update(self, serializer):
        """Ensure user_id is preserved on update"""
        user_id = get_user_id_from_request(self.request)
        serializer.save(user_id=user_id)


class TimelineViewSet(viewsets.ModelViewSet):
    serializer_class = TimelineSerializer
    
    def get_queryset(self):
        """Filter timelines by user_id through their vision"""
        user_id = get_user_id_from_request(self.request)
        # Filter timelines where the vision belongs to this user
        return Timeline.objects.filter(vision__user_id=user_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Ensure timeline's vision belongs to the user"""
        user_id = get_user_id_from_request(self.request)
        vision = serializer.validated_data.get('vision')
        
        # Verify vision belongs to user
        if vision and vision.user_id != user_id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only create timelines for your own visions.")
        
        serializer.save()