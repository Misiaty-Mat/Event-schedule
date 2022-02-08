from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.sign_up_user, name='register'),
    path('login/', views.loginuser, name='login'),
    path('make-event/', views.make_event, name='make_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('logout/', views.logoutuser, name='logout'),
    path('del-event/<int:event_id>', views.del_event, name='delete_event'),
    path('event/<int:event_id>', views.detail_event, name='detail_event'),
]
