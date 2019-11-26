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
    solvers = models.ManyToManyField(User, related_name='solver')

    def __str__(self):
        return self.title

class Solution(models.Model):

    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=DEFAULT_TASK_ID)
    answer = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    verdict = EnumField(Virdict, max_length=500,default=Virdict.WRONG_ANSWER)
    submitTime = models.DateTimeField(default=datetime.timezone.now(), blank=True)
    need_rang = models.IntegerField()
    comments = ArrayField(models.CharField(max_length=2000), blank=True, default=list())

class ImageModel(models.Model):

    class Meta:
        verbose_name =  "ImageModel"
        verbose_name_plural =  "ImageModels"

    image = models.ImageField(upload_to = 'uploads/contest/sol_images', default='uploads/contest/no_images.jpg')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

class Contest(models.Model):

    class Meta:
        verbose_name = "Contest"
        verbose_name_plural = "Contests"

    def __str__(self):
        return self.name

    def task_default():
        return [1]

    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, through='TaskContestCase')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    team_size = models.IntegerField(default=4)
    startDate = models.DateTimeField(default=datetime.timezone.now(), blank=True)
    finishDate = models.DateTimeField(default=datetime.timezone.now(), blank=True)
    contestants = models.ManyToManyField(User, through='ContestUser', related_name='contestants')          
  

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
    name = models.CharField(max_length=200)
    rangs = models.ManyToManyField(User, through='Rang')


class Theme(models.Model):

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, through='TaskCase')
    general_theme = models.ManyToManyField(GlobalTheme, through='GlobalThemeName')
    def __str__(self):
    	return str(self.name)

class GlobalThemeName(models.Model):
    hardness = models.IntegerField()
    global_them = models.ForeignKey(GlobalTheme, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

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

    points = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

class Rang(models.Model):

    class Meta:
        verbose_name = "Rang"
        verbose_name_plural = "Rangs"

    point = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.ForeignKey(GlobalTheme, on_delete=models.CASCADE)

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
    inlines = (TaskCase_inline, TaskContestCase_inline)

class ThemeAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline, GlobalThemeName_inline)
class GlobalThemeAdmin(admin.ModelAdmin):
    inlines = (GlobalThemeName_inline, )

