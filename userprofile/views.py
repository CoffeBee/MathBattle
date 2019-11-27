from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import ProfileForm, UserForm, TeamForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Team
import hashlib

@login_required(login_url='../auth/login/')
def profile_views(request):
  if request.method == 'POST':
    form = TeamForm(request.POST)
    if form.is_valid():
      m = hashlib.md5()
      m.update(form.cleaned_data['name'].encode('utf-8'))
      if (Team.objects.filter(name = form.cleaned_data['name']).exists()):
          return redirect('/userprofile/team/{}'.format(str(m.hexdigest())))
      newteam = Team(name = form.cleaned_data['name'], link = str(m.hexdigest()))
      newteam.save()
      newteam.users.add(request.user)
      newteam.save()
      return redirect('/userprofile/team/{}'.format(str(m.hexdigest())))
  return HttpResponse(render(request,'contest/userprofile.html',
							  {"email" : request.user.email,
							   "username" : request.user.username,
							   "first_name": request.user.profile.first_name,
							   "second_name": request.user.profile.second_name,
							   "father_name": request.user.profile.father_name,
							   "school": request.user.profile.school,
							   "location": request.user.profile.location,
							   "grade": request.user.profile.grade, 'form' : TeamForm()}))

@login_required(login_url='../auth/login/')
def team(request, team_name):
	team = Team.objects.get(link=team_name)
	if request.method == 'POST':
		if not request.user in team.users.all():
			team.users.add(request.user)
	return render(request, 'contest/team.html', {'team' : team,
                                                'user' : request.user,
                                                "first_name": request.user.profile.first_name,
                 							    "second_name": request.user.profile.second_name,
                                                "school": request.user.profile.school,
                                                "grade": request.user.profile.grade,})

@login_required(login_url='../auth/login/')
@transaction.atomic
def update_profile(request):
	if request.method == 'POST':
		user_form=UserForm(request.POST, instance=request.user)
		profile_form=ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(
				request, ('Your profile was successfully updated!'))
			return HttpResponseRedirect('/userprofile')
		else:
			messages.error(request, ('Please correct the error below.'))
	else:
		user_form=UserForm(instance=request.user)
		profile_form=ProfileForm(instance=request.user.profile)
	return render(request, 'contest/update_profiles.html', {
		'user_form': user_form,
		'profile_form': profile_form
	})
