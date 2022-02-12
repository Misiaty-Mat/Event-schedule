from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.sign_up_user, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
]
