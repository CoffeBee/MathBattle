# Generated by Django 2.2.5 on 2019-11-10 10:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20191110_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='finishDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 10, 58, 41, 742274, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contest',
            name='startDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 10, 58, 41, 742247, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='solution',
            name='submitTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 10, 58, 41, 741454, tzinfo=utc)),
        ),
    ]