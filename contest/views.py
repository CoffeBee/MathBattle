from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.db.models import Q
from django.db.models.functions import datetime

from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution, Contest
from checker.virdicts import Virdict
from .forms import CheckForm

@login_required(login_url='../../auth/login/')
def themes(request):
    themes = Theme.objects.all() 
    return render(request, 'contest/index.html', context={'themes': themes, 'user' : request.user})

@login_required(login_url='../../../auth/login/')
def theme(request, theme_name):
	tasks = TaskCase.objects.filter(theme__name=theme_name).all()
	return render(request, 'contest/theme.html', context={'theme' : tasks, 'user' : request.user})

@login_required(login_url='../../../auth/login')
def contests(request):
    contests = Contest.objects.filter(finishDate__date__gte=datetime.timezone.now())
    return render(request, 'contest/contests.html', context={'contests' : contests, 'user' : request.user})

@login_required(login_url='../../../auth/login')
def contest(request, contest_name):
    contest = Contest.objects.get(name=contest_name)
    return render(request, 'contest/contest.html', context={'contest' : contest, 'user' : request.user})

@login_required(login_url='../../auth/login/')
def solutions(request):
    submits = Solution.objects.filter(verdict=Virdict.ACCEPTED_FOR_EVUALETION).filter(~Q(username=request.user)).filter(task__solvers=request.user).all()
    return render(request, 'contest/solutions.html', context={'submits': submits, 'user' : request.user})

@login_required(login_url='../../../auth/login/')
def solution(request, submit_id):
    submit = Solution.objects.get(id=submit_id)
    if (submit.username == request.user):
        return render(request, 'contest/ownSolutionJudge.html', context={'submit': submit, 'user' : request.user})
    if (submit.verdict != Virdict.ACCEPTED_FOR_EVUALETION):
    	return render(request, 'contest/solutionError.html')
    if (request.method == 'POST'):
        form = CheckForm(request.POST)  
        if form.is_valid():
            if 'OK' in request.POST:
                submit.task.solvers.add(request.user)
                submit.verdict = Virdict.ACCEPTED
                submit.judgerComment = form.cleaned_data['comment']
            else:
                submit.verdict = Virdict.REJECTED
                submit.judgerComment = form.cleaned_data['comment']
            submit.save()
            return redirect('/themes/solutions')

    return render(request, 'contest/solutionJudge.html', context={'submit': submit, 'form' : CheckForm(), 'user' : request.user})
