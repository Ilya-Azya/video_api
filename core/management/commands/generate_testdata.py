from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from videos.models import Video


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        for i in range(5):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f"{username}@example.com",
                                                password="testpass123")
            else:
                user = User.objects.get(username=username)
            for j in range(3):
                Video.objects.create(
                    name=f"Video {j} by user{i}",
                    owner=user
                )
        self.stdout.write(self.style.SUCCESS("Test data generated."))
