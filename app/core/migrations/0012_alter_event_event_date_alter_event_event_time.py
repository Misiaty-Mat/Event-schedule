# Generated by Django 4.0.1 on 2022-01-28 10:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 28, 10, 44, 52, 752738, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(default=datetime.datetime(2022, 1, 28, 10, 44, 52, 752765, tzinfo=utc)),
        ),
    ]
