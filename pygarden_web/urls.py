from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('apps.accounts.urls')),
    path('rosliny/', include('apps.plants.urls')),
    path('zadania/', include('apps.scheduler.urls')),
    path('obserwacje/', include('apps.observations.urls')),
    path('statystyki/', include('apps.analytics.urls')),
    path('', RedirectView.as_view(pattern_name='plants:list', permanent=False)),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
