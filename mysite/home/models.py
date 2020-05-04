import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    canvas_token = models.CharField(max_length=2000, default='', blank=True)
    calender_link = models.CharField(max_length=2000, default='', blank=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    def __str__(self):
        return self.user.username
