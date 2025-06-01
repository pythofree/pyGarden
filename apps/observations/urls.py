from django.urls import path
from . import views

app_name = 'observations'

urlpatterns = [
    path('', views.ObservationListView.as_view(), name='list'),
    path('dodaj/', views.ObservationCreateView.as_view(), name='add'),
    path('<int:pk>/edytuj/', views.ObservationUpdateView.as_view(), name='edit'),
    path('<int:pk>/usun/', views.ObservationDeleteView.as_view(), name='delete'),
]
