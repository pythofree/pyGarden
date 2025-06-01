from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    # Список всех растений текущего пользователя
    path('', views.PlantListView.as_view(), name='list'),
    # Создание нового растения
    path('dodaj/', views.PlantCreateView.as_view(), name='add'),
    # Детальный просмотр (по ID)
    path('<int:pk>/', views.PlantDetailView.as_view(), name='detail'),
    # Редактирование растения (по ID)
    path('<int:pk>/edytuj/', views.PlantUpdateView.as_view(), name='edit'),
    # Удаление растения (по ID)
    path('<int:pk>/usun/', views.PlantDeleteView.as_view(), name='delete'),
]
