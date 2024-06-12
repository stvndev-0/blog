from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    body = models.TextField(max_length=15000)
    date_create = models.DateField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.CharField(max_length=255)
    date_create = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)