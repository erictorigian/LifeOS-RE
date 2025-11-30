from rest_framework import serializers
from .models import Block
import uuid


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = "__all__"

    def create(self, validated_data):
        # Auto-generate timeline_id if none provided
        if "timeline_id" not in validated_data or validated_data["timeline_id"] is None:
            validated_data["timeline_id"] = uuid.uuid4()

        return super().create(validated_data)