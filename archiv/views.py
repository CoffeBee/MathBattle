from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from task.models import Task
def archive(request):
    task = Task.objects.all()
    task_href = []
    for i in range(1, len(task)):
        task_href.append([i, task[i - 1].title])
    template = loader.get_template('contest/archive.html')
    return HttpResponse(template.render({"tasks": task_href, 'username' : request.user.username}, request))

