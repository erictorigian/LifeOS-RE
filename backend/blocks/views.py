from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Max
from backend.auth_utils import get_user_id_from_request

from .models import Block
from .serializers import BlockSerializer


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    
    def get_queryset(self):
        """Filter blocks by user_id from authenticated user"""
        user_id = get_user_id_from_request(self.request)
        return Block.objects.filter(user_id=user_id)
    
    def perform_create(self, serializer):
        """Automatically set user_id when creating a block"""
        user_id = get_user_id_from_request(self.request)
        serializer.save(user_id=user_id)
    
    def perform_update(self, serializer):
        """Ensure user_id is preserved on update"""
        user_id = get_user_id_from_request(self.request)
        serializer.save(user_id=user_id)

    @action(detail=False, methods=["get"])
    def latest(self, request):
        """
        Returns the latest block for the authenticated user.
        """
        user_id = get_user_id_from_request(self.request)
        block = Block.objects.filter(user_id=user_id).order_by("-created_at").first()

        return Response(BlockSerializer(block).data if block else None)