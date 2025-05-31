from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Приложение accounts: регистрация, вход, профиль
    path('accounts/', include('apps.accounts.urls')),

    # Здесь позже будут другие приложения:
    # path('plants/', include('apps.plants.urls')),
    # ...

    # Редирект с корня на, например, страницу входа (или другую)
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
