from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.models import ContestUser
from userprofile.models import Team
import random
from django.db.models import Q
from django.db.models.functions import datetime
from django.utils import timezone
from .forms import ContestRegister
from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution, Contest, Rang, TaskContestCase
from checker.virdicts import Virdict
from .forms import CheckForm
def check(task, user):
    if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.ACCEPTED).exists():
        return 1
    if Solution.objects.filter(username=user, task=task.task).exists():
        return 2
    return 0
def check_team(task, team):
    fl = 0
    for user in team.users.all():
        if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.ACCEPTED).exists():
            return 1
        if Solution.objects.filter(username=user, task=task.task).exists():
            fl = 2
    return fl
    
@login_required(login_url='../../auth/login/')
def themes(request):
    themes = Theme.objects.all() 
    return render(request, 'contest/index.html', context={'themes': themes, 'user' : request.user})

@login_required(login_url='../../../auth/login/')
def theme(request, theme_name):
    tasks = [[check(task, request.user), task] for task in TaskCase.objects.filter(theme__name=theme_name).all()]
    return render(request, 'contest/theme.html', context={'theme' : tasks, 'user' : request.user})

@login_required(login_url='../../../auth/login')
def contests(request):
    contests = Contest.objects.filter(finishDate__date__gte=datetime.timezone.now())
    return render(request, 'contest/contests.html', context={'contests' : contests, 'user' : request.user})

@login_required(login_url='../../../auth/login')
def contest(request, contest_name):

        
    now = timezone.now()
    contest = Contest.objects.get(name = contest_name)
    if request.method == "POST":
        team = Team.objects.get(pk=request.POST['team'])
        new_contest_user = ContestUser(team = team, user = request.user, point=0, contest = contest)
        new_contest_user.save()
    if now > contest.startDate and now < contest.finishDate:
        if len(ContestUser.objects.filter(contest=contest, user=request.user).all()) == 0:
            return render(request, 'contest/ContestRegister.html', context={'form' : ContestRegister(user=request.user)})
        team = ContestUser.objects.get(contest=contest, user=request.user).team
        score = 0
        Mayscore = 0
        for task in contest.tasks.all():
            mfl = False
            sfl = False
            for user in team.users.all():
                if not sfl and Solution.objects.filter(username = user).filter(verdict = Virdict.ACCEPTED).filter(task = task).exists():
                    score += TaskContestCase.objects.get(task=task, contest__name=contest_name).points
                    sfl = True
                if not mfl and Solution.objects.filter(username = user).filter(Q(verdict = Virdict.ACCEPTED_FOR_EVUALETION_IN_CONTEST) | Q(verdict = Virdict.ACCEPTED) | Q(verdict = Virdict.ACCEPTED_FOR_EVUALETION)).filter(task = task).exists():
                    Mayscore += TaskContestCase.objects.get(task=task, contest__name=contest_name).points
                    mfl = True
        tasks = [[check_team(task, team), task] for task in TaskContestCase.objects.filter(contest__name=contest_name).all()]
        return render(request, 'contest/contest.html', context={'tasks' : tasks, 'user' : request.user, 'score' : score, 'Mayscore' : Mayscore})
    return render(request, 'contest/solutionError.html')


@login_required(login_url='../../auth/login/')
def solutions(request):
    solutions = Solution.objects.all()
    need = []
    for sol in  solutions:
        if len(sol.task.theme_set.all()) == 0:
            continue
        theme = sol.task.theme_set.all()[0]
        global_theme = theme.general_theme.all()[0]
        rang = 0
        try:
            rang = Rang.objects.get(user=request.user, theme=global_theme).point
        except:
            pass
        if rang > sol.need_rang and sol.username != request.user and (sol.verdict == Virdict.ACCEPTED_FOR_EVUALETION or sol.verdict == Virdict.APPLICATION or sol.verdict == Virdict.ACCEPTED_FOR_EVUALETION):
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
    	return render(request, 'contest/ContestError.html')
    if (request.method == 'POST'):
        form = CheckForm(request.POST)  
        if form.is_valid():
            if 'OK' in request.POST:
                submit.task.solvers.add(request.user)
                submit.verdict = Virdict.ACCEPTED
                l = list(submit.comments)
                print(l)
                l.append(form.cleaned_data['comment'])
                submit.comments = l
            else:
                submit.verdict = Virdict.REJECTED
                submit.comments.append(form.cleaned_data['comment'])
            submit.save()
            return redirect('/themes/solutions')

    return render(request, 'contest/solutionJudge.html', context={'submit': submit, 'form' : CheckForm(), 'user' : request.user})
