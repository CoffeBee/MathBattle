from django import forms
from django.contrib.auth import authenticate, get_user_model


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Вы не зарегистрированы ;(')
            if not user.check_password(password):
                raise forms.ValidationError('Вы забыли пароль')
            if not user.is_active:
                raise forms.ValidationError('Вы слегка за бортом')
        return super().clean(*args, **kwargs)


User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Ваш ник')
    email = forms.EmailField(label='Ваш e-mail адрес')
    password = forms.CharField(widget=forms.PasswordInput, label='Ваш пароль')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                'Этот e-mail уже привязан к другому аккаунту')
        return super().clean(*args, **kwargs)
