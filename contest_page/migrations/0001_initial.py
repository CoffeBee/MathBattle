# Generated by Django 2.1.2 on 2019-02-17 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_1_id', models.IntegerField()),
                ('task_2_id', models.IntegerField()),
                ('task_3_id', models.IntegerField()),
                ('task_4_id', models.IntegerField()),
                ('task_5_id', models.IntegerField()),
                ('task_6_id', models.IntegerField()),
                ('duraction', models.IntegerField()),
            ],
        ),
    ]