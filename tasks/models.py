from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from checker.virdicts import Virdict
from checker.models import Checker
from enumfields import EnumField, Enum
from django.db.models.functions import datetime
from django_summernote.fields import SummernoteTextField

# Create your models here.

DEFAULT_THEME_ID = 1
DEFAULT_TASK_ID = 1
DEFAULT_CHECKER_ID = 1

class Hardness(Enum):
    JUNIOR = 'JUNIOR'
    MIDDLE_JUNIOR = 'MIDDLE-JUNIOR'
    MIDDLE = 'MIDDLE'
    MIDDLE_SINIOR = 'MIDDLE-SINIOR'
    SINIOR = 'SINIOR'
    SINIOR_UPPER = 'SINIOR-UPPER'



class Task(models.Model):

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    text = models.CharField(max_length=2000, verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    right_answer = models.CharField(max_length=200, verbose_name='Правильный ответ')
    checker = models.ForeignKey(Checker, on_delete=models.CASCADE, default=DEFAULT_CHECKER_ID, verbose_name='Проверяющая программа')
    title = models.CharField(default='Task', max_length=200, verbose_name='Название')
    solvers = models.ManyToManyField(User, related_name='solver', verbose_name='Список решивших')
    answer_only = models.BooleanField(default=False, verbose_name="Проверять только ответы")

    def __str__(self):
        return self.title

class Message(models.Model):
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
    text = SummernoteTextField()

class Solution(models.Model):

    class Meta:
        verbose_name = "Решение"
        verbose_name_plural = "Решения"

    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=DEFAULT_TASK_ID, verbose_name='Задача')
    answer = models.CharField(max_length=2000, verbose_name='Ответ')
    description = SummernoteTextField(verbose_name='Решение')
    verdict = EnumField(Virdict, max_length=500,default=Virdict.WRONG_ANSWER, verbose_name='Вердикт')
    submitTime = models.DateTimeField(default=datetime.timezone.now(), blank=True, verbose_name='Время')
    need_rang = models.IntegerField(verbose_name='Ранг проверки')
    comments = models.ManyToManyField(Message, blank=True, verbose_name='Комментарии жури')
    themesol = models.ForeignKey("Theme", on_delete=models.CASCADE, verbose_name="Решение по теме")

class Contest(models.Model):

    class Meta:
        verbose_name = "Контест"
        verbose_name_plural = "Контесты"

    def __str__(self):
        return self.name

    def task_default():
        return [1]

    name = models.CharField(max_length=200, verbose_name='Название')
    tasks = models.ManyToManyField(Task, through='TaskContestCase', verbose_name='Задачи')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    team_size = models.IntegerField(default=4, verbose_name='Ограничение на количество человек в команде')
    startDate = models.DateTimeField(default=datetime.timezone.now(), blank=True, verbose_name='Время начала контеста')
    finishDate = models.DateTimeField(default=datetime.timezone.now(), blank=True, verbose_name='Время окончания контеста')
    contestants = models.ManyToManyField(User, through='ContestUser', related_name='contestants', verbose_name='Участники')


class ContestUser(models.Model):

    class Meta:
        verbose_name = "ContestUser"
        verbose_name_plural = "ContestUsers"

    def __str__(self):
        pass
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    team = models.ForeignKey('userprofile.Team', on_delete=models.CASCADE)
    point = models.IntegerField()


class GlobalTheme(models.Model):

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Раздел"

    name = models.CharField(max_length=200, verbose_name='Название')
    rangs = models.ManyToManyField(User, through='Rang', verbose_name='Ранг')
    def __str__(self):
        return str(self.name)

class Theme(models.Model):

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    name = models.CharField(max_length=200, verbose_name='Название')
    tasks = models.ManyToManyField(Task, through='TaskCase', verbose_name='Задачи')
    general_theme = models.ManyToManyField(GlobalTheme, through='GlobalThemeName', verbose_name='Раздел')
    def __str__(self):
    	return str(self.name)

class GlobalThemeName(models.Model):
    hardness = models.IntegerField(verbose_name='Сложность')
    global_them = models.ForeignKey(GlobalTheme, on_delete=models.CASCADE, verbose_name='Раздел')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='Тема')



class TaskCase(models.Model):

    class Meta:
        verbose_name = "TaskCase"
        verbose_name_plural = "TasksCase"

    hardness = EnumField(Hardness, max_length=500, default=Hardness.MIDDLE, verbose_name='Сложность')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='Тема')


class TaskContestCase(models.Model):

    class Meta:
        verbose_name = "TaskContestCase"
        verbose_name_plural = "TaskContestCases"

    points = models.IntegerField(verbose_name='Стоимость')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, verbose_name='Контест')

class Rang(models.Model):

    class Meta:
        verbose_name = "Ранг"
        verbose_name_plural = "Ранги"

    point = models.IntegerField(verbose_name='Очки крутости')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    theme = models.ForeignKey(GlobalTheme, on_delete=models.CASCADE, verbose_name='Раздел')

class Points(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

class TaskContestCase_inline(admin.TabularInline):
    model = TaskContestCase
    extra = 1

class TaskCase_inline(admin.TabularInline):
    model = TaskCase
    extra = 1

class GlobalThemeName_inline(admin.TabularInline):
    model = GlobalThemeName
    extra = 1

class ContestAdmin(admin.ModelAdmin):
    inlines = (TaskContestCase_inline,)

class TaskAdmin(admin.ModelAdmin):
    exclude = ('solvers', "author",)
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
        obj.solvers.add(request.user)
        obj.save()
    inlines = (TaskCase_inline, TaskContestCase_inline)

class ThemeAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline, GlobalThemeName_inline)
class GlobalThemeAdmin(admin.ModelAdmin):
    inlines = (GlobalThemeName_inline, )
