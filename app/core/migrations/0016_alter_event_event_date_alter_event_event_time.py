# Generated by Django 4.0.1 on 2022-02-01 17:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_event_image_alter_event_event_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]