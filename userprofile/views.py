from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tasks.models import Theme, TaskCase
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import ProfileForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

def profile_views(request):
        return HttpResponse(render(request,'contest/userprofile.html', {"email" : request.user.email, "username" : request.user.username, "themes": Theme.objects.all(), "taskcase" : TaskCase.objects.all()}))

"""def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            return HttpResponse('image upload success')
"""
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect('/userprofile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'userprofile/update_profiles/index.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

    
