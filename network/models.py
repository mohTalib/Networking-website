from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=200)
    time = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} By {self.user} on {self.time.strftime('%d %b %Y %H:%M:%S')}"

class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")

    def __str__(self):
        return f"{self.user_following} following {self.user_followers}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLike")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postLike")

    def __str__(self):
        return f"{self.user} Liked {self.post}"