from django import forms
from .models import *

class SolForm(forms.ModelForm):
    answer = forms.CharField(max_length=100, label="You answer", widget=forms.TextInput(attrs={'class': "form-control"}))
    description = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder':"Чудесные мысли", 'class':"form-control char-textarea", 'data-length':1000}))

    class Meta:
        model = Solution
        fields = ('answer', 'description', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"class" : "file filestyle", "id" : "file"}), label="")    
    class Meta:
        model = ImageModel
        fields = ('image', )
