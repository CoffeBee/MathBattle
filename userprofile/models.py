from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Theme

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    father_name = models.CharField(max_length=50, blank=True)
    school = models.TextField(max_length=100, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.second_name + ' ' + self.first_name + ' ' +self.father_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Rang(models.Model):
    name = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.name

class UserRang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    rang = models.ForeignKey(Rang, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ' ' + str(self.rang) + ' ' + str(self.theme)
