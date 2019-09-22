from django import forms

class NumSolveForm(forms.Form):

    answer = forms.CharField(max_length=100, label="You answer")
