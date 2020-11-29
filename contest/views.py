from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from tasks.models import ContestUser
from userprofile.models import Team
import random
from django.core import serializers
from django.db.models import Q
from django.db.models.functions import datetime
from django.utils import timezone
from .forms import ContestRegister
from django.contrib.auth.decorators import login_required
from tasks.models import Theme, TaskCase, Solution, Contest, Rang, TaskContestCase, Message, GlobalThemeName, Task
from checker.virdicts import Virdict
from .forms import CheckForm
import logging
import time
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Get an instance of a logger

from django.core.serializers.json import DjangoJSONEncoder


def main(request):
    if (request.user_agent.is_mobile):
        return render(request, "contest/mobile/about.html")
    return render(request, 'contest/about.html')

logger = logging.getLogger('ok')
def check(task, user):
    if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.ACCEPTED).exists():
        return 1
    if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.ACCEPTED_FOR_EVUALETION).exists():
        return 3
    if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.APPLICATION).exists():
        return 3
    if Solution.objects.filter(username=user, task=task.task).exists():
        return 2
    return 0

def solved(task):
    return len(Solution.objects.filter(task=task.task, verdict = Virdict.ACCEPTED))
def submited(task):
    return len(Solution.objects.filter(task=task.task))
def check_team(task, team):
    fl = 0
    for user in team.users.all():
        if Solution.objects.filter(username=user, task=task.task, verdict = Virdict.ACCEPTED).exists():
            return 1
        if Solution.objects.filter(username=user, task=task.task).exists():
            fl = 2
    return fl

def get_theme_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        themes = Theme.objects.filter(
            Q(name__icontains=q)
        ).distinct()
    for theme in themes:
        queryset.append(theme)
    return list(set(queryset))
def hard(t):
    return GlobalThemeName.objects.get(global_them=t.general_theme.all()[0], theme=t).hardness
def progress(t, request):
    cnt_all = 0
    cnt = 0

    for i in t.tasks.all():
        cnt_all += 1
        if (Solution.objects.filter(verdict=Virdict.ACCEPTED).filter(username=request.user).filter(task=i).count() > 0):
            cnt += 1
    if cnt_all == 0:
        return 100
    return int(cnt * 100 / cnt_all)
@login_required(login_url='../../auth/login/')
def themes(request):
    if request.user.is_superuser:
        themes = Theme.objects.all()
    else:
        themes = Theme.objects.filter(start_time__lt=datetime.timezone.now())
    themes_clean = [(hard(theme), theme, progress(theme, request)) for theme in themes]
    if request.GET:
        query = request.GET['q']
        themes = get_theme_queryset(query)
    if (request.user_agent.is_mobile):
        return render(request, 'contest/mobile/index.html', context={'themes': themes, 'user': request.user})
    return render(request, 'contest/index.html', context={'themes': themes_clean, 'user': request.user})

def tabletheme(request, themename):
    theme = Theme.objects.filter(name=themename).first()
    tasks = theme.tasks.all()
    solutions = Solution.objects.filter(themesol=theme)
    need = {}
    i = 1
    taskI = {}
    for task in tasks:
        taskI[task] = i
        i += 1
    for sol in solutions:
        if sol.verdict == Virdict.PREVIEW:
            continue
        user = sol.username
        if user not in need.keys():
            tasksres = []
            tasksres.append(0)
            for task in tasks:
                tasksres.append('х')
            need[user] = tasksres
        verdict = sol.verdict
        if verdict == Virdict.WRONG_ANSWER and need[user][taskI[sol.task]] == 'х':
            need[user][taskI[sol.task]] = '-'
        if verdict == Virdict.ACCEPTED_FOR_EVUALETION and (need[user][taskI[sol.task]] == 'х' or need[user][taskI[sol.task]] == '-'):
            need[user][taskI[sol.task]] = '?'
        if verdict == Virdict.IN_EVUALETION and (need[user][taskI[sol.task]] == 'х' or need[user][taskI[sol.task]] == '-'):
            need[user][taskI[sol.task]] = '?'
        if verdict == Virdict.REJECTED and need[user][taskI[sol.task]] == 'х':
            need[user][taskI[sol.task]] = '-'
        if verdict == Virdict.ACCEPTED:
            need[user][0] += 1
            need[user][taskI[sol.task]] = '+'
        if verdict == Virdict.APPLICATION and (need[user][taskI[sol.task]] == ' ' or need[user][taskI[sol.task]] == '-'):
            need[user][taskI[sol.task]] = '?'
    return need

@login_required(login_url='../../../auth/login/')
def theme(request, theme_name):
    tasks = [[check(task, request.user), task, solved(task), submited(task)] for task in TaskCase.objects.filter(theme__name=theme_name).all()]
    thema = Theme.objects.filter(name=theme_name).first()
    context = {"theme": tasks, "user": request.user, "tabledata": tabletheme(request, theme_name), 'active': thema.deadline > timezone.now()}
    if (request.user_agent.is_mobile):
        return render(request, 'contest/mobile/theme.html', context)
    return render(request, 'contest/theme.html', context)

@login_required(login_url='../../../auth/login')
def contests(request):
    contests = Contest.objects.filter(finishDate__date__gte=datetime.timezone.now())
    if (request.user_agent.is_mobile):
        return render(request, 'contest/mobile/contests.html', context={'contests' : contests, 'user' : request.user})
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
        team = ContestUser.objects.filter(contest=contest, user=request.user).all()[0].team
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
        tasks = [[check_team(task, team), task, solved(task), submited(task)] for task in TaskContestCase.objects.filter(contest__name=contest_name).all()]
        if (request.user_agent.is_mobile):
            return render(request, 'contest/mobile/contest.html', context={'tasks' : tasks, 'user' : request.user, 'score' : score, 'Mayscore' : Mayscore, 'name' : tasks[0][1].contest.name})
        return render(request, 'contest/contest.html', context={'tasks' : tasks, 'user' : request.user, 'score' : score, 'Mayscore' : Mayscore, 'name' : tasks[0][1].contest.name})
    return render(request, 'contest/solutionError.html')


@login_required(login_url='../../auth/login/')
def solutions(request):
    solutions = Solution.objects.filter(~(Q(verdict = Virdict.PREVIEW) | Q(verdict = Virdict.ACCEPTED)))
    paginator = Paginator(solutions, 24)
    need = []
    if request.user.is_superuser:
        need = paginator.page(1)
    if (request.user_agent.is_mobile):
        return render(request, 'contest/mobile/solutions.html', context={'submits': need, 'user' : request.user})
    return render(request, 'contest/solutions.html', context={'submits': need, 'user' : request.user, 'pageNumber' : paginator.num_pages})

def solutionspage(request, page):
    solutions = Solution.objects.filter(~(Q(verdict = Virdict.PREVIEW) | Q(verdict = Virdict.ACCEPTED)))
    paginator = Paginator(solutions, 24)
    if request.user.is_superuser:
        solutions = Solution.objects.all()
        return JsonResponse(serializers.serialize('json', Paginator(solutions, 24).page(page), fields=('id', 'task', 'task__title', 'submitTime', 'username', 'answer'), use_natural_foreign_keys=True, use_natural_primary_keys=True), safe=False)
    else:
        return JsonResponse({ "Auth" : False }, safe=False)
@login_required(login_url='../../../auth/login/')
def solution(request, submit_id):
    submit = Solution.objects.get(id=submit_id)
    if (submit.username == request.user):
        if (submit.verdict == Virdict.REJECTED):
            if (request.method == 'POST'):
                form = CheckForm(request.POST)
                if form.is_valid():
                    new_message = Message(text=form.cleaned_data['comment'])
                    new_message.save()
                    submit.verdict = Virdict.APPLICATION
                    submit.comments.add(new_message)
                    submit.need_rang += 1
                    submit.save()
                return redirect('/themes/solutions')
            if (request.user_agent.is_mobile):
                return render(request, 'contest/mobile/ownSolutionJudgeReject.html', context={'submit': submit, 'user' : request.user, 'form' : CheckForm()})
            return render(request, 'contest/ownSolutionJudgeReject.html', context={'submit': submit, 'user' : request.user, 'form' : CheckForm()})
        if (request.user_agent.is_mobile):
            return render(request, 'contest/mobile/ownSolutionJudge.html', context={'submit': submit, 'user' : request.user})
        return render(request, 'contest/ownSolutionJudge.html', context={'submit': submit, 'user' : request.user})
    if (submit.verdict != Virdict.ACCEPTED_FOR_EVUALETION and submit.verdict != Virdict.APPLICATION):
    	return render(request, 'contest/ContestError.html')
    theme = submit.task.theme_set.all()[0]
    global_theme = theme.general_theme.all()[0]
    rang = 0
    try:
        rang = Rang.objects.get(user=request.user, theme=global_theme).point
    except:
        pass

    if (request.method == 'POST'):
        form = CheckForm(request.POST)
        if form.is_valid():
            new_message = Message(text=form.cleaned_data['comment'])
            new_message.save()
            if 'OK' in request.POST:
                logs = open("okknig", 'a')
                logs.write("{} сдал задачу из темы {} под названием {}. Принимал {}. Время {}".format(submit.username.username, theme.name, submit.task.title, request.user.username, time.time()))
                logs.close()
                submit.task.solvers.add(request.user)
                submit.verdict = Virdict.ACCEPTED
                submit.comments.add(new_message)
            else:
                submit.verdict = Virdict.REJECTED
                submit.comments.add(new_message)
            submit.save()
            return redirect('/themes/solutions')
    
    if (request.user_agent.is_mobile):
        return render(request, 'contest/mobile/solutionJudge.html', context={'submit': submit, 'form' : CheckForm(), 'user' : request.user})
    return render(request, 'contest/solutionJudge.html', context={'submit': submit, 'form' : CheckForm(), 'user' : request.user, 'task' : submit.task.title})
