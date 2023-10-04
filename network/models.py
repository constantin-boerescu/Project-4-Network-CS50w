from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} was made by {self.user} at {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_by")
    post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")

    def __str__(self):
        return f"Like {self.id}. {self.user} liked {self.post}"