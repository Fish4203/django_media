# Generated by Django 3.0.5 on 2020-05-05 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_userprofile_canvas_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='canvas_token',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]