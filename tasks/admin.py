from django.contrib import admin
from .models import Task, Theme, TaskAdmin, ThemeAdmin, Solution, Contest, ContestAdmin
# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Solution)