from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Theme


class Profile(models.Model):

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, blank=True, verbose_name="Имя")
    second_name = models.CharField(max_length=50, blank=True, verbose_name="Фамилия")
    father_name = models.CharField(max_length=50, blank=True, verbose_name="Очество")
    school = models.TextField(max_length=100, blank=True, verbose_name="Школа")
    location = models.CharField(max_length=30, blank=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    grade = models.IntegerField(null=True, blank=True, verbose_name="Класс")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Team(models.Model):

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    users = models.ManyToManyField(User, verbose_name="Игроки")
    name = models.CharField(max_length=2000, verbose_name="Название")
    link = models.CharField(max_length=200, verbose_name="Ссылка")
