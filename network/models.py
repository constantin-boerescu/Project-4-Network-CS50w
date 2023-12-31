from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return f"Post {self.id} was made by {self.author} at {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Following(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_that_follows")
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")

    def __str__(self):
        return f"User {self.user} follows {self.followed_user}"