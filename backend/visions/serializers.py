from rest_framework import serializers
from .models import Vision, Timeline


class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'
        read_only_fields = ['created_at']