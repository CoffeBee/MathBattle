from django import forms
from userprofile.models import Team
class CheckForm(forms.Form):
	comment = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder':"Чудесные мысли", 'class':"form-control char-textarea", 'data-length':1000}))

class ContestRegister(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ContestRegister, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ChoiceField(
            choices=[(o.id, o.name) for o in user.team_set.all()], 
            widget=forms.Select(attrs={'class' : 'custom-select form-control', 'style' : 'margin : 30px; margin-top : 10px; margin-bottom : 10px;'})
        )
        	