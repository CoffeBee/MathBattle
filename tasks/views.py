from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

from .models import Task, Solution
from .forms import NumSolveForm
from checker.models import Checker
from checker.virdicts import Virdict
def task(request, theme_name, task_title):
    task = Task.objects.get(title=task_title)
    submits = Solution.objects.filter(task=task, username=request.user)
    if  request.method == 'POST':
        form = NumSolveForm(request.POST)  
        if (form.is_valid()):
            ans = form.cleaned_data['ans']
            description = form.cleaned_data['description']
            checker = task.checker
            if checker.checkAns(ans, task.right_answer):
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED_FOR_EVUALETION, task=task)
            else:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.WRONG_ANSWER, task=task)
            newsol.save()
            
    return render(request, 'contest/task.html', context={'themename' : theme_name, 'task' : task, 'form' : NumSolveForm(), 'submits' : submits})
    
