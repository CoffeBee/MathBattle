from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.functions import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from pytz import unicode

# Create your models here.

class Contest:
	def task_default():
		return [1]