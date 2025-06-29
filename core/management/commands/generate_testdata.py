from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from videos.models import Video
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        for i in range(5):
            user = User.objects.create_user(username=f"user{i}", email=f"user{i}@example.com", password="testpass123")
            for j in range(3):
                Video.objects.create(
                    title=f"Video {j} by user{i}",
                    description="A sample video",
                    owner=user
                )
        self.stdout.write(self.style.SUCCESS("Test data generated."))
