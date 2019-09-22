from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from .models import SupInformation

def profile_views(request):
        return HttpResponse(render(request,'contest/userprofile.html', {"email" : request.user.email, "username" : request.user.username}))

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():

            return HttpResponse('image upload success')
