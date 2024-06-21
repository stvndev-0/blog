from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


# Creamos el perfil del cliente
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', default='default.jpg', null=True)
        
    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover/', null=True)
    body = models.TextField(max_length=15000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        return f'{self.title} by {self.author.username}'

class Comment(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment on {self.post.title} by {self.author.username}'