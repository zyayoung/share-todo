from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'todo'

urlpatterns = [
    path('todo/', login_required(views.TodoListView.as_view()), name='todo-list'),
    path('done/', login_required(views.DoneListView.as_view()), name='done-list'),
    path('todo/<int:pk>', login_required(views.TodoDetailView.as_view()), name='todo-detail'),
    path('', views.IndexView.as_view(), name='index'),
    path('alt/<int:pk>', views.alt, name='alt'),
    path('calendar/', login_required(views.CalendarView.as_view()), name='calendar'),
    path('api/event/', views.event),
]
