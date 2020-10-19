from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .models import Task, Solution, Rang, GlobalThemeName, TaskContestCase
from checker.models import Checker
from checker.virdicts import Virdict
from .forms import TaskForm
from django.utils import timezone
from django.db.models import Q


@login_required(login_url='../../../auth/login/')
def task(request, task_title):
     task = Task.objects.filter(title=task_title)[0]
     submits = Solution.objects.filter(task=task, username=request.user).filter(~Q(verdict = Virdict.PREVIEW))
     if  request.method == 'POST':
        form = TaskForm(request.POST)
        if (True):
            form.is_valid()
            ans = form.cleaned_data['answer']
            description = ''
            if 'description' in form.cleaned_data.keys():
                description = form.cleaned_data['description']


            checker = task.checker
            rang = 0
            try:
                rang = Rang.objects.get(user=request.user, theme=task.theme_set.all()[0].general_theme.all()[0]).point
            except:
                 pass
            if "preview" in request.POST:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.PREVIEW, task=task, need_rang=rang, themesol=task.theme_set.all()[0])
                newsol.save()
                return redirect('../../themes/solutions/{}'.format(newsol.id))
            if task.theme_set.all()[0].deadline < timezone.now():
                pass
            elif checker.checkAns(ans, task.right_answer):
             if task.answer_only:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED, task=task, need_rang=rang, themesol=task.theme_set.all()[0])
             else:
                newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.ACCEPTED_FOR_EVUALETION, task=task, need_rang=rang, themesol=task.theme_set.all()[0])
            else:
             newsol = Solution(username=request.user, answer=ans, description=description, verdict=Virdict.WRONG_ANSWER, task=task, need_rang=rang, themesol=task.theme_set.all()[0])
            newsol.save()
     if (request.user_agent.is_mobile):
         return render(request, 'contest/mobile/task.html', context={'task' : task, 'form' : TaskForm(), 'submits' : submits, 'active': task.theme_set.all()[0].deadline > timezone.now()})
     return render(request, 'contest/task.html', context={'task' : task, 'form' : TaskForm(), 'submits' : submits, 'active' : task.theme_set.all()[0].deadline > timezone.now()})
