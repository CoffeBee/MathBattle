# Generated by Django 2.2.5 on 2019-09-22 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organiration', models.CharField(max_length=100)),
                ('grade', models.CharField(default='None', max_length=100)),
                ('photo', models.ImageField(upload_to='')),
            ],
        ),
    ]
