from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Task, Solution, Rang, GlobalThemeName, TaskContestCase
from .forms import NumSolveForm
from checker.models import Checker
from checker.virdicts import Virdict

@login_required(login_url='../../../auth/login/')
def task(request, task_title):

    task = Task.objects.get(title=task_title)
    submits = Solution.objects.filter(task=task, username=request.user)
    if  request.method == 'POST':
        form = NumSolveForm(request.POST, request.FILES)
        if (form.is_valid()):
            ans = form.cleaned_data['ans']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            checker = task.checker
            rang = 0
            try:
                rang = Rang.objects.get(user=request.user, theme=task.theme_set.all()[0].general_theme.all()[0]).point
            except:
                pass
            print(rang)
            print(TaskContestCase.objects.filter(task=task))
            is_right = checker.checkAns(ans, task.right_answer)
            if is_right and not TaskContestCase.objects.filter(task=task).exists():
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED_FOR_EVUALETION, task=task, need_rang=rang, comments=[], model_pic=image)
            elif is_right:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED_FOR_EVUALETION_IN_CONTEST, task=task, need_rang=rang, comments=[], model_pic=image)
            else:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.WRONG_ANSWER, task=task, need_rang=rang, comments=[], model_pic=image)
            newsol.save()

    return render(request, 'contest/task.html', context={'task' : task, 'form' : NumSolveForm(), 'submits' : submits})
