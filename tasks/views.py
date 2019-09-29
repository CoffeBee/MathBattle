from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Task, Solution
from .forms import NumSolveForm
from .checker import Checker
def task(request, theme_name, task_title):
    task = Task.objects.get(title=task_title)
    return render(request, 'contest/task.html', context={'themename' : theme_name, 'task' : task})
    
