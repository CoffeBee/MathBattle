from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from checker.virdicts import Virdict
from checker.models import Checker
from enumfields import EnumField, Enum

from django.db.models.functions import datetime

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
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    text = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    right_answer = models.CharField(max_length=200)
    checker = models.ForeignKey(Checker, on_delete=models.CASCADE, default=DEFAULT_CHECKER_ID)
    title = models.CharField(default='Task', max_length=200)

    def __str__(self):
        return self.title

class Solution(models.Model):

    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2000)
    description = models.CharField(max_length=20000)
    verdict = EnumField(Virdict, max_length=500,default=Virdict.WRONG_ANSWER)
    
class Contest(models.Model):

    class Meta:
        verbose_name = "Contest"
        verbose_name_plural = "Contests"

    def __str__(self):
        pass

    def task_default():
        return [1]

    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, through='TaskContestCase')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    team_size = models.IntegerField(default=4)
    startDate = models.DateTimeField(default=datetime.timezone.now(), blank=True)
    finishDate = models.DateTimeField(default=datetime.timezone.now(), blank=True)          
    
class Theme(models.Model):

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, through='TaskCase')
    general_name = models.CharField(max_length=200, default='Геометрия')
    hardness = EnumField(Hardness, max_length=500, default=Hardness.MIDDLE)
    def __str__(self):
    	return str(self.name)

class TaskCase(models.Model):

    class Meta:
        verbose_name = "TaskCase"
        verbose_name_plural = "TasksCase"

    hardness = EnumField(Hardness, max_length=500, default=Hardness.MIDDLE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    

class TaskContestCase(models.Model):

    class Meta:
        verbose_name = "TaskContestCase"
        verbose_name_plural = "TaskContestCases"

    def __str__(self):
        pass

    points = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

class TaskContestCase_inline(admin.TabularInline):
    model = TaskContestCase
    extra = 1

class TaskCase_inline(admin.TabularInline):
    model = TaskCase
    extra = 1

class ContestAdmin(admin.ModelAdmin):
    inlines = (TaskContestCase_inline,)

class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline, TaskContestCase_inline)

class ThemeAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline,)




    