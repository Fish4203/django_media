# Generated by Django 3.0.5 on 2020-05-03 11:37

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200503_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='canvas_token',
            field=fernet_fields.fields.EncryptedTextField(),
        ),
    ]