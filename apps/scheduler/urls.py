from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('dodaj/', views.TaskCreateView.as_view(), name='add'),
    path('<int:pk>/edytuj/', views.TaskUpdateView.as_view(), name='edit'),
    path('<int:pk>/usun/', views.TaskDeleteView.as_view(), name='delete'),
]
