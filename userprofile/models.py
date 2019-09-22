from django.db import models


class SupInformation(models.Model):
    organiration = models.CharField(max_length=100)
    grade = models.CharField(default="None", max_length=100)
    photo = models.ImageField()
