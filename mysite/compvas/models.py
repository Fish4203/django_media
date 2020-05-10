import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield import JSONField
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

class CachSites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.IntegerField()
    class_info = models.OneToOneField(Class_info, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='', blank=True)
    course_code = models.CharField(max_length=100, default='', blank=True)
    image_download_url = models.CharField(max_length=100, null=True)

    class_json = JSONField()
    assign_json = JSONField()
    modules_json = JSONField()
    frontpage_json = JSONField()
    files_json = JSONField()

    def __str__(self):
        return str(self.class_id)
