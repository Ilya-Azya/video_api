from django.contrib import admin

from .models import Video, VideoFile


class VideoFileInline(admin.TabularInline):
    model = VideoFile
    extra = 1


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_published', 'total_likes', 'created_at')
    list_filter = ('is_published', 'created_at', 'owner')
    search_fields = ('name', 'owner__username')
    inlines = [VideoFileInline]


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ('video', 'quality', 'file')
    list_filter = ('quality',)
