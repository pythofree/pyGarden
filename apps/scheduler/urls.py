from django.urls import path
from . import views
from . import calendar_views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('dodaj/', views.TaskCreateView.as_view(), name='add'),
    path('<int:pk>/edytuj/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:pk>/usun/', views.TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/wykonaj/', views.mark_done, name='mark_done'),

    path('kalendarz/', calendar_views.task_calendar_view, name='calendar'),
    path('kalendarz/json/', calendar_views.calendar_events_json, name='calendar_json'),
    path('kalendarz/dzien/<str:date>/', views.task_list_for_day_view, name='calendar_day'),
]
