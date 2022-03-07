from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from libgravatar import Gravatar

from core.models import User
from core.forms import SearchForUserForm


class SearchForUser(TemplateView):
    form_class = SearchForUserForm
    template_name = "search_for_user.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, event_id, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            users_match = request.POST['username']
            return redirect('found_users', event_id, users_match)
        return render(request, self.template_name, {'form': form})
        


class FoundUsers(TemplateView):
    template_name = 'user_list.html'
    def get(self, request, event_id, users_match, *args, **kwargs):
        users = User.objects.filter(username__istartswith=users_match)
        users_plus_icons = [(user, Gravatar(user.email).get_image()) for user in users]
        print(users_plus_icons)
        return render(request, self.template_name, {'users': users_plus_icons})
