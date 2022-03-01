from django.contrib.auth import forms as auth_form
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from datetime import datetime, date

from core import models


class RegisterForm(auth_form.UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ('username', 'email',)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.DateInput):
    input_type = 'time'


class MakeEventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['title', 'description', 'event_date', 'event_time', 'image']
        widgets = {
             'event_date': DateInput(),
            'event_time': TimeInput(),
        }


    def clean(self):
        cd = self.cleaned_data
        if cd.get('event_date') and cd.get('event_time'):
            days_until_event = (cd.get('event_date') - date.today()).days
            minute_counter = (datetime.combine(datetime.today(), cd.get('event_time')) - datetime.now()).total_seconds()
            if days_until_event < 0:
                self.add_error('event_date', forms.ValidationError(_("Event can not be created earlier than today."), code='invalid'))
            elif days_until_event == 0 and minute_counter < 0:
                self.add_error('event_time', forms.ValidationError(_("Events can not be created in past time."), code='invalid'))
            del days_until_event
            del minute_counter
        return cd
        
