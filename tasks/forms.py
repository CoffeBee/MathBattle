from django import forms

class NumSolveForm(forms.Form):
	ans = forms.CharField(max_length=100, label="You answer", widget=forms.TextInput(attrs={'class': "form-control"}))
	description = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder':"Чудесные мысли", 'class':"form-control char-textarea", 'data-length':1000}))