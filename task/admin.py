from django.contrib import admin
from .models import Task, Theme, TaskAdmin, ThemeAdmin
# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Theme, ThemeAdmin)