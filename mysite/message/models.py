import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Comments(models.Model):
    comment_text = models.CharField(max_length=200)
    comment_link = models.ManyToManyField('self')
    #comment_post = models.ForeignKey(Posts, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.comment_text

class Posts(models.Model):
    title_text = models.CharField(max_length=200)
    body_text = models.CharField(max_length=2000)
    img_link = models.CharField(max_length=500, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date published')
    comment_link = models.ManyToManyField(Comments)

    def is_recent(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title_text
