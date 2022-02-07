from django.contrib.auth import forms as auth_form
from django import forms
from django.contrib.auth.models import User

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
        
