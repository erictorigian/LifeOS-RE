from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Max

from .models import Block
from .serializers import BlockSerializer


class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    @action(detail=False, methods=["get"])
    def latest(self, request):
        """
        Returns the latest block for the user.
        """
        user_id = request.query_params.get("user_id")
        block = Block.objects.filter(user_id=user_id).order_by("-created_at").first()

        return Response(BlockSerializer(block).data if block else None)