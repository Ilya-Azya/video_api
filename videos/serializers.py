from rest_framework import serializers
from .models import Video, VideoFile, Like


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ['id', 'file', 'quality']


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    files = VideoFileSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'owner', 'name', 'is_published', 'total_likes', 'created_at', 'files']
