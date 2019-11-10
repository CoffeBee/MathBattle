# Generated by Django 2.2.5 on 2019-11-10 08:44

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20191110_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2000), blank=True, default=[''], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contest',
            name='finishDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 8, 43, 54, 514459, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contest',
            name='startDate',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 8, 43, 54, 514430, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='solution',
            name='description',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='solution',
            name='submitTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 10, 8, 43, 54, 513535, tzinfo=utc)),
        ),
    ]