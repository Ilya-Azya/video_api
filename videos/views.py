from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, Subquery, OuterRef
from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Video, Like
from .serializers import VideoSerializer, VideoFileSerializer

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().prefetch_related('files')
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(total_likes=0)

    def get_permissions(self):
        if self.action in ['like', 'unlike']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Video.objects.all()
        elif user.is_authenticated:
            return Video.objects.filter(models.Q(is_published=True) | models.Q(owner=user))
        else:
            return Video.objects.filter(is_published=True)

    @action(detail=True, methods=['post'], url_path='likes')
    def like(self, request, pk=None):
        video = self.get_object()
        like, created = Like.objects.get_or_create(video=video, user=request.user)
        if created:
            Video.objects.filter(pk=video.pk).update(total_likes=models.F('total_likes') + 1)
            return Response({'status': 'liked'})
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        video = self.get_object()
        deleted, _ = Like.objects.filter(video=video, user=request.user).delete()
        if deleted:
            Video.objects.filter(pk=video.pk).update(total_likes=models.F('total_likes') - 1)
            return Response({'status': 'unliked'})
        return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='upload-file')
    def upload_file(self, request, pk=None):
        video = self.get_object()

        if video.owner != request.user and not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = VideoFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(video=video)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoIDsView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Video.objects.filter(is_published=True).values_list('id', flat=True)

    def list(self, request, *args, **kwargs):
        return Response(list(self.get_queryset()))


class VideoStatisticsSubqueryView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        published_videos = Video.objects.filter(is_published=True)
        likes_sum_subquery = published_videos.filter(owner=OuterRef('pk')).values('owner') \
            .annotate(sum_likes=Sum('total_likes')).values('sum_likes')
        data = User.objects.annotate(likes_sum=Subquery(likes_sum_subquery)).order_by('-likes_sum') \
            .values('username', 'likes_sum')
        return Response(data)


class VideoStatisticsGroupByView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        data = User.objects.filter(videos__is_published=True) \
            .annotate(likes_sum=Sum('videos__total_likes')) \
            .values('username', 'likes_sum').order_by('-likes_sum')
        return Response(data)
