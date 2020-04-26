import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Posts(models.Model):
    title_text = models.CharField(max_length=200)
    body_text = models.CharField(max_length=2000)
    img_link = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')

    def is_recent(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title_text
