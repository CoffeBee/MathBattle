from django.shortcuts import render
from django.http import HttpResponse
import random
from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase


@login_required(login_url='../auth/login/')
def themes(request):
    themes = Theme.objects.all() 
    return render(request, 'contest/index.html', context={'themes': themes})

@login_required(login_url='../auth/login/')
def theme(request, theme_name):
	tasks = TaskCase.objects.filter(theme__name=theme_name).all()
	return render(request, 'contest/theme.html', context={'theme' : tasks})