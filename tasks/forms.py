from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class TaskForm(forms.Form):
    answer = forms.CharField(max_length=100, label="You answer", widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(widget=SummernoteWidget())
