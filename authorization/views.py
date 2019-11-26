from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    next = request.GET.get('next')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/themes/theme')
        return render(request, 'authorization/loginFailed.html', context={'form' : UserLoginForm()})

    return render(request, 'authorization/login.html', context={'form' : UserLoginForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        user = authenticate(username=user.username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    elif (request.method == "POST"):
        return render(request, 'authorization/registerFailed.html')

    context = {
        'form': form,
    }
    return render(request, 'authorization/register.html', context)
