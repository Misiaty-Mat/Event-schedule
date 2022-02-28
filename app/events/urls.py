from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('make-event/', views.make_event, name='make_event'),
    path('events/', views.my_events, name='my_events'),
    path('old-events/', views.old_events, name='old_events'),
    path('del-event/<int:event_id>', views.del_event, name='delete_event'),
    path('events/<int:event_id>', views.detail_event, name='detail_event'),
    path('events/edit/<int:event_id>', views.edit_event, name='edit_event'),
]
