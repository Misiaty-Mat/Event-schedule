from django.shortcuts import render, redirect
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
    render_page_var_dict = {'form': MakeEventForm(request.POST, request.FILES), 'events': get_quick_events(request)}
    if request.method == 'GET':
        return render(request, 'events/make_events.html', render_page_var_dict)
    else:
        if request.POST['title'] == '':
                render_page_var_dict['error'] = "You must give a title to the event"
                return render(request, 'events/make_events.html', render_page_var_dict)
        try:
            days_until_event = (datetime.strptime(request.POST['event_date'],'%Y-%m-%d') - datetime.now()).days + 1
            minute_counter = (datetime.strptime(request.POST['event_date'] + ' ' + \
                request.POST['event_time'],'%Y-%m-%d %H:%M') - datetime.now()).total_seconds()
            if days_until_event < 0:
                render_page_var_dict['error'] = "Event can not be created earlier than today"
                return render(request, 'events/make_events.html', render_page_var_dict)
            elif days_until_event == 0 and minute_counter < 0:
                render_page_var_dict['error'] = "Events can not be created in past time"
                return render(request, 'events/make_events.html', render_page_var_dict)

            form = MakeEventForm(request.POST, request.FILES)
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
            return render(request, 'events/make_events.html', render_page_var_dict)
        except ValueError:
            render_page_var_dict['error'] = "You must specify a time of the event"
            return render(request, 'events/make_events.html', render_page_var_dict)

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
    event = Event.objects.get(id=event_id, user=request.user)
    return render(request, 'events/detail-event.html', {'event': event})