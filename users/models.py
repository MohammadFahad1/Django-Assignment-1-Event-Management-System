from django.db import models
from django.contrib.auth.models import AbstractUser
        
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='profile_images/default_profile.png')
    phone = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)