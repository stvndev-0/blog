from django.db import models
from django.contrib.auth.models import User

# Creamos el perfil del cliente
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='default.jpg', null=True, blank=True)
    
    def __str__(self):
        return self.user.username