from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('eksport/json/', views.export_json, name='export_json'),

    # Вход и выход (используем стандартные вьюхи Django)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),

    # Просмотр профиля
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Редактирование профиля
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    # По желанию: смена пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]
