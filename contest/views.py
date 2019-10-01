from django.shortcuts import render
from django.http import HttpResponse
import random
from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution
from checker.virdicts import Virdict


@login_required(login_url='../auth/login/')
def themes(request):
    themes = Theme.objects.all() 
    return render(request, 'contest/index.html', context={'themes': themes})

@login_required(login_url='../auth/login/')
def theme(request, theme_name):
	tasks = TaskCase.objects.filter(theme__name=theme_name).all()
	return render(request, 'contest/theme.html', context={'theme' : tasks})

@login_required(login_url='../auth/login/')
def solutions(request):
    submits = Solution.objects.filter(verdict=Virdict.ACCEPTED_FOR_EVUALETION)
    print(submits)
    return render(request, 'contest/solutions.html', context={'submits': submits})