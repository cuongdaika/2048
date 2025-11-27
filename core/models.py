from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_seconds = models.FloatField(help_text="Thời gian chơi tính bằng giây")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"