from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.db.models import Q
from django.db.models.functions import datetime

from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution, Contest, Rang
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
    solutions = Solution.objects.all()
    need = []
    for sol in  solutions:
        theme = sol.task.theme_set.all()[0]
        global_theme = theme.general_theme.all()[0]
        rang = 0
        try:
            rang = Rang.objects.get(user=request.user, theme=global_theme).point
        except:
            pass
        if rang > sol.need_rang and sol.username != request.user and (sol.verdict == Virdict.ACCEPTED_FOR_EVUALETION or sol.verdict == Virdict.APPLICATION):
            need.append(sol)
    return render(request, 'contest/solutions.html', context={'submits': need, 'user' : request.user})

@login_required(login_url='../../../auth/login/')
def solution(request, submit_id):
    submit = Solution.objects.get(id=submit_id)
    print(submit.verdict)
    if (submit.username == request.user):
        if (submit.verdict == Virdict.REJECTED):
            if (request.method == 'POST'):
                form = CheckForm(request.POST)  
                if form.is_valid():
                    submit.verdict = Virdict.APPLICATION
                    submit.comments.append(form.cleaned_data['comment'])
                    submit.need_rang += 1
                    submit.save()
                return redirect('/themes/solutions')
            return render(request, 'contest/ownSolutionJudgeReject.html', context={'submit': submit, 'user' : request.user})
        return render(request, 'contest/ownSolutionJudge.html', context={'submit': submit, 'user' : request.user})
    if (submit.verdict != Virdict.ACCEPTED_FOR_EVUALETION and submit.verdict != Virdict.APPLICATION):
    	return render(request, 'contest/solutionError.html')
    if (request.method == 'POST'):
        form = CheckForm(request.POST)  
        if form.is_valid():
            if 'OK' in request.POST:
                submit.task.solvers.add(request.user)
                submit.verdict = Virdict.ACCEPTED
                submit.comments.apppend(form.cleaned_data['comment'])
            else:
                submit.verdict = Virdict.REJECTED
                submit.comments.append(form.cleaned_data['comment'])
            submit.save()
            return redirect('/themes/solutions')

    return render(request, 'contest/solutionJudge.html', context={'submit': submit, 'form' : CheckForm(), 'user' : request.user})
