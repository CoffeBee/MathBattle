from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

DEFAULT_THEME_ID = 1


class Theme(models.Model):

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    name = models.CharField(max_length=200)



class Task(models.Model):
    text = models.CharField(max_length=2000)
    author = models.CharField(max_length=100)
    right_answer = models.CharField(max_length=200)
    typetype = models.IntegerField()
    title = models.CharField(default='Task', max_length=200)


class Solves(models.Model):
    username = models.CharField(max_length=100)
    answer = models.CharField(max_length=2000)
    task_id = models.IntegerField(default=0)
    isRight = models.BooleanField(null=True)
