from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(
        blank=True, 
        upload_to=f'profile/{nickname}'
    )
    
class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
    