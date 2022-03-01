from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from datetime import datetime

from core.models import Event
from core.forms import MakeEventForm


def get_quick_events(request):
    """Function to get 5 most close events to user"""
    user_events = None
    if request.user.is_authenticated:
        user_events =  Event.objects.filter(user=request.user, event_date__gte=datetime.today()).order_by('event_date')[:5]
        event_num = len(user_events)
        event_counter = ['One', 'Two', 'Three', 'Four', 'Five'][:event_num]
        user_events = dict(zip(event_counter, user_events))
    return user_events

def home(request):
    return render(request, 'events/index.html', {'events': get_quick_events(request)})

@login_required
def make_event(request):
    form = MakeEventForm(request.POST, request.FILES)
    near_events = get_quick_events(request)
    if request.method == 'GET':
        return render(request, 'events/make_events.html', {'form': form, 'events': near_events})
    else:
        try:
            form = MakeEventForm(request.POST, request.FILES)
            if form.is_valid():
                new_event = form.save(commit=False)
                new_event.user = request.user
                new_event.save()
                return redirect('home')
            raise(ValueError)
        except ValueError:
            return render(request, 'events/make_events.html', {'form': form, 'events': near_events})

@login_required
def my_events(request):
    if request.method == 'GET':
        today = datetime.today()
        events = Event.objects.filter(user=request.user, event_date__gte=today).order_by('event_date')
        return render(request, 'events/my_events.html', {'events': events, 'today': today.date})

@login_required
def old_events(request):
    if request.method == 'GET':
        today = datetime.today()
        events = Event.objects.filter(user=request.user, event_date__lt=today).order_by('-event_date')
        return render(request, 'events/old_events.html', {'events': events, 'today': today.date})

@login_required
def del_event(request, event_id):
    if request.method == 'POST':
        Event.objects.get(id=event_id).delete()
        return redirect('my_events')

@login_required
def detail_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'GET':
        return render(request, 'events/detail_event.html', {'event': event})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'GET':
        form = MakeEventForm(instance=event)
        return render(request, 'events/edit_event.html', {'event': event, 'form': form})
    else:
        try:
            form = MakeEventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                return redirect('my_events')
            raise(ValueError)
        except ValueError:
            return render(request, 'events/edit_event.html', {'event': event, 'form': form})
