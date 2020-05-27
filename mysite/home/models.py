import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    phone_num = models.CharField(max_length=10, default='', blank=True)

    def __str__(self):
        return self.user.username
