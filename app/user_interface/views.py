from django.db import IntegrityError
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from . import forms

from core.models import User, Event

from datetime import datetime


def home(request):
    user_events = None
    if request.user.is_authenticated: 
        user_events =  Event.objects.filter(user=request.user, event_date__gte=datetime.today()).order_by('event_date')[:5]
    return render(request, 'ui/index.html', {'events': user_events})

def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'ui/signUpUser.html', {'form': forms.RegisterForm()})
    else:
        try:
            validate_email(request.POST['email'])
        except ValidationError:
            return render(
                request, 'ui/signUpUser.html',
                {'form': forms.RegisterForm(request.POST), 'error': 'Enter valid email.'}
            )
        else:
            if request.POST['password1'] == request.POST['password2']:
                if len(request.POST['password1']) < 6:
                    return render(
                        request, 'ui/signUpUser.html',
                        {'form': forms.RegisterForm(request.POST), 'error': 'Password must be at least 6 characters long.'}
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
                        request, 'ui/signUpUser.html',
                        {'form': forms.RegisterForm(request.POST), 'error': 'Username or email is already taken.'}
                    )
            else:
                return render(
                    request, 'ui/signUpUser.html',
                    {'form': forms.RegisterForm(request.POST), 'error': 'Passwords did not match.'}
                )

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'ui/login.html', {'form': AuthenticationForm()})
    else:
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('home')
        except AttributeError:
            return render(request, 'ui/login.html', {'form': AuthenticationForm(request.POST), 'error': "Username or password are incorrect"})

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
            form = forms.MakeEventForm(request.POST, request.FILES)
            if form.is_valid():
                new_event = Event.objects.create(
                    title=form.cleaned_data.get('title'),
                    description=form.cleaned_data.get('description'),
                    event_date=form.cleaned_data.get('event_date'),
                    event_time=form.cleaned_data.get('event_time'),
                    user=request.user,
                    image=form.cleaned_data.get('image')
                )
                new_event.save()
                return redirect('home')
            return render(request, 'ui/make_events.html', {'form': forms.MakeEventForm(), 'error': "Invalid data in form"})

@login_required
def my_events(request):
    if request.method == 'GET':
        today = datetime.today()
        events = Event.objects.filter(user=request.user, event_date__gte=today).order_by('event_date')
        return render(request, 'ui/my_events.html', {'events': events, 'today': today.date})
