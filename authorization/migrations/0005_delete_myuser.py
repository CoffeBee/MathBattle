# Generated by Django 2.1.5 on 2019-03-02 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_auto_20190302_1210'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]