from django.db import IntegrityError
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from . import forms

from core.models import User


def home(request):
    return render(request, 'ui/index.html')

def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'ui/signUpUser.html', {'form': forms.RegisterForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(
                    request, 'ui/signUpUser.html',
                    {'form': forms.RegisterForm(), 'error': 'Username or email is already taken.'}
                )
        else:
            return render(
                request, 'ui/signUpUser.html',
                {'form': forms.RegisterForm(), 'error': 'Passwords did not match.'}
            )

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'ui/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ui/login.html', {'form': AuthenticationForm(), 'error': "Username or password are incorrect"})
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')