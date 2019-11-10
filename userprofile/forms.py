from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name',
                  'second_name',
                  'father_name',
                  'location',
                  'birth_date',
                  'school',
                  'grade',
                  )