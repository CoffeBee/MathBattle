from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Task, Solution, Rang, GlobalThemeName, TaskContestCase, ImageModel
from .forms import SolForm, ImageForm
from checker.models import Checker
from checker.virdicts import Virdict
import secrets
def handle_uploaded_file(f):
    path = secrets.token_urlsafe(16)
    path =  'uploads/contest/{}.'.format(path)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path

@login_required(login_url='../../../auth/login/')
def task(request, task_title):
    ImageFormSet = modelformset_factory(ImageModel, form=ImageForm, extra=5)
    task = Task.objects.get(title=task_title)
    submits = Solution.objects.filter(task=task, username=request.user)
    return render(request, 'contest/task.html', context={'task' : task, 'form' : SolForm(), 'submits' : submits, 'imForm' : ImageFormSet(queryset=ImageModel.objects.none())})
