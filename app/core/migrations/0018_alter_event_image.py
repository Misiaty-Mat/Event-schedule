# Generated by Django 4.0.1 on 2022-02-01 18:04

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.event_image_file_path),
        ),
    ]