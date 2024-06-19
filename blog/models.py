from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Creamos el perfil del cliente
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/', null=True)
        
    def __str__(self):
        return self.user.username
    
# Creamos un perfil de usuario de forma predeterminada cuando el usuario se registra
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
# Automatiza el perfil
post_save.connect(create_profile, sender=User)

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