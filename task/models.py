from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
# Create your models here.

DEFAULT_THEME_ID = 1
DEFAULT_TASK_ID = 1

class Task(models.Model):

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    text = models.CharField(max_length=2000)
    author = models.CharField(max_length=100)
    right_answer = models.CharField(max_length=200)
    typetype = models.IntegerField()
    title = models.CharField(default='Task', max_length=200)

    def __str__(self):
        return self.title

class Theme(models.Model):

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"

    name = models.CharField(max_length=200)
    tasks = models.ManyToManyField(Task, through='TaskCase')
    def __str__(self):
    	return str(self.name)

class TaskCase(models.Model):

    class Meta:
        verbose_name = "TaskCase"
        verbose_name_plural = "TasksCase"

    level = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

class Solution(models.Model):

    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"

    username = models.CharField(max_length=100)
    answer = models.CharField(max_length=2000)
    task_id = models.IntegerField(default=0)
    isRight = models.BooleanField(null=True)

class TaskCase_inline(admin.TabularInline):
    model = TaskCase
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline,)

class ThemeAdmin(admin.ModelAdmin):
    inlines = (TaskCase_inline,)

    