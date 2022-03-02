from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import SearchForUser, FoundUsers

urlpatterns = [
    path('search', login_required(SearchForUser.as_view()), name='search_for_user'),
    path('users/<str:users_match>', login_required(FoundUsers.as_view()), name='found_users'),
]

