from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 
from django.contrib.auth.decorators import login_required

from .models import Task, Solution, Rang, GlobalThemeName
from .forms import NumSolveForm
from checker.models import Checker
from checker.virdicts import Virdict

@login_required(login_url='../../../auth/login/')
def task(request, theme_name, task_title):
    task = Task.objects.get(title=task_title)
    submits = Solution.objects.filter(task=task, username=request.user)
    if  request.method == 'POST':
        form = NumSolveForm(request.POST)  
        if (form.is_valid()):
            ans = form.cleaned_data['ans']
            description = form.cleaned_data['description']
            checker = task.checker
            rang = 0
            try:
                rang = Rang.objects.get(user=request.user, theme=task.theme_set.all()[0].general_theme.all()[0]).point
            except:
                pass
            print(rang)
            if checker.checkAns(ans, task.right_answer):
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED_FOR_EVUALETION, task=task, need_rang=rang)
            else:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.WRONG_ANSWER, task=task, need_rang=rang)
            newsol.save()
            
    return render(request, 'contest/task.html', context={'themename' : theme_name, 'task' : task, 'form' : NumSolveForm(), 'submits' : submits})
    
