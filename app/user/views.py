from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from core.models import User
from core.forms import RegisterForm

def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'user/sign_up.html', {'form': RegisterForm()})
    try:
        validate_email(request.POST['email'])
    except ValidationError:
        return render(
            request, 'user/sign_up.html',
            {'form': RegisterForm(request.POST), 'error': 'Enter valid email.'}
        )
    else:
        if request.POST['password1'] == request.POST['password2']:
            if len(request.POST['password1']) < 6:
                return render(
                    request, 'user/sign_up.html',
                    {'form': RegisterForm(request.POST), 'error': 'Password must be at least 6 characters long.'}
                )
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
                    request, 'user/sign_up.html',
                    {'form': RegisterForm(request.POST), 'error': 'Username or email is already taken.'}
                )
        return render(
            request, 'user/sign_up.html',
            {'form': RegisterForm(request.POST), 'error': 'Passwords did not match.'}
        )

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'user/login.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('home')
        except AttributeError:
            return render(
                request,
                'user/login.html',
                {'form': AuthenticationForm(request.POST), 'error': "Username or password are incorrect"})

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')