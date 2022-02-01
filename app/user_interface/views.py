from django.db import IntegrityError
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from . import forms

from core.models import User, Event

from datetime import datetime


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

@login_required
def make_event(request):
    if request.method == 'GET':
        return render(request, 'ui/make_events.html', {'form': forms.MakeEventForm()})
    else:
        days_until_event = (datetime.strptime(request.POST['event_date'],'%Y-%m-%d') - datetime.now()).days + 1
        minute_counter = (datetime.strptime(request.POST['event_date'] + ' ' + \
            request.POST['event_time'],'%Y-%m-%d %H:%M') - datetime.now()).total_seconds()

        if days_until_event < 0:
            return render(request, 'ui/make_events.html', {'form': forms.MakeEventForm(), 'error': "Event can not be created earlier than today"})
        elif days_until_event == 0 and minute_counter < 0:
            return render(request, 'ui/make_events.html', {'form': forms.MakeEventForm(), 'error': "Events can not be created in past time"})
        else:
            form = forms.MakeEventForm(request.POST)
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect('home')

@login_required
def my_events(request):
    if request.method == 'GET':
        today = datetime.today()
        events = Event.objects.filter(user=request.user, event_date__gte=today).order_by('event_date')
        return render(request, 'ui/my_events.html', {'events': events, 'today': today.date})
