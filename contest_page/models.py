from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.
from django.db.models.functions import datetime
from pytz import unicode

class Contest(models.Model):
    def task_default():
        return [1]
    tasks = ArrayField(models.IntegerField(), blank=True, default=task_default)
    author = models.CharField(max_length=100, default="People")
    team_size = models.IntegerField(default=4)
    dateST = models.DateTimeField(default=datetime.timezone.now(), blank=True)
    dateED = models.DateTimeField(default=datetime.timezone.now(), blank=True)
