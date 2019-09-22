from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Contest
from django.template import loader
from django.utils.timezone import now
from task.models import Task, Solves
def contest(request, contest_id):
    contest = Contest.objects.all()[contest_id - 1]
    task = Task.objects.all()
    if (contest.dateST < now() and contest.dateED > now() or True):
        tasks = contest.tasks
        while (tasks[-1] == -1):
            tasks.pop()
        names = []
        numbers = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in tasks:
            names.append([task[i - 1].title])
        for i in range(0, len(names)):
            names[i].append(tasks[i])
            names[i].append(numbers[i - 1])
        res = 0
        for j in range(len(tasks)):
            old_solves = Solves.objects.filter(username=request.user.id, task_id=tasks[j]).all()
            for i in old_solves:
                if (i.isRight):
                    res += 500 * (j + 1)
                    break
        template = loader.get_template('contest/contest_page_start.html')
        return HttpResponse(template.render({"tasks": names, 'res' : res, 'username' : request.user.username}, request))
    elif contest.dateST > now() :
        template = loader.get_template('contest/contest_page_notstart.html')
        return HttpResponse(template.render({},request))
    else:
        template = loader.get_template('contest/contest_page_end.html')
        return HttpResponse(template.render({}, request))
