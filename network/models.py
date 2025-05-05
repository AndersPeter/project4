from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")

    def save(self):
        if self.user == self.user_follower:
            raise ValidationError("You can't follow yourself")
        else:
            super().save()

    class Meta:
        unique_together = ("user", "user_follower")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
