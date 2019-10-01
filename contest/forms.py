from django import forms

class CheckForm(forms.Form):
	comment = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder':"Чудесные мысли", 'class':"form-control char-textarea", 'data-length':1000}))
