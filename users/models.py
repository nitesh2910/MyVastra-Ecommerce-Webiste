from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    profile_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default-user.png', blank=True)

    def __str__(self):
        return self.user.username
