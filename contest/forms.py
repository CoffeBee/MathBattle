from django import forms
from userprofile.models import Team
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CheckForm(forms.Form):
	comment = forms.CharField(widget=SummernoteWidget())

class ContestRegister(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ContestRegister, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ChoiceField(
            choices=[(o.id, o.name) for o in user.team_set.all()],
            widget=forms.Select(attrs={'class' : 'custom-select form-control', 'style' : 'margin : 30px; margin-top : 10px; margin-bottom : 10px;'})
        )
