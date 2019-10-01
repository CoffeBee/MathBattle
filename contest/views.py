from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution
from checker.virdicts import Virdict
from .forms import CheckForm

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
    submits = Solution.objects.filter(verdict=Virdict.ACCEPTED_FOR_EVUALETION).filter(~Q(username=request.user)).all()
    print(submits)
    return render(request, 'contest/solutions.html', context={'submits': submits})

@login_required(login_url='../auth/login/')
def solution(request, submit_id):
    submit = Solution.objects.get(id=submit_id)
    if (submit.verdict != Virdict.ACCEPTED_FOR_EVUALETION):
    	return render(request, 'contest/solutionError.html')
    if (request.method == 'POST'):
        form = CheckForm(request.POST)  
        if form.is_valid():
            if 'OK' in request.POST:
                submit.verdict = Virdict.ACCEPTED
                submit.comment = form.cleaned_data['comment']
            else:
                submit.verdict = Virdict.REJECTED
                submit.comment = form.cleaned_data['comment']
            submit.save()
            return redirect('/themes/solutions')
    if (submit.username == request.user):
        return render(request, 'contest/ownSolutionJudge.html', context={'submit': submit})
    return render(request, 'contest/solutionJudge.html', context={'submit': submit, 'form' : CheckForm()})
