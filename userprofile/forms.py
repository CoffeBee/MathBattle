from django import forms
from django.contrib.auth import authenticate, get_user_model

class ImageUploadForm(forms.Form):
    image = forms.ImageField()