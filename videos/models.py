from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    total_likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class VideoFile(models.Model):
    QUALITY_CHOICES = [
        ('HD', '720p'),
        ('FHD', '1080p'),
        ('UHD', '4K'),
    ]

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='videos/')
    quality = models.CharField(max_length=3, choices=QUALITY_CHOICES)

    def __str__(self):
        return f"{self.video.name} ({self.quality})"

class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('video', 'user')