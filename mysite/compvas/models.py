import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Class_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.IntegerField()
    notes = models.TextField(default='', blank=True)
    compass_link = models.CharField(max_length=100, default='', blank=True)
    google_sites = models.CharField(max_length=100, default='', blank=True)
    other_resource = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return str(self.class_id)
