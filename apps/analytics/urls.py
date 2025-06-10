from django.urls import path
from .views import *

app_name = 'analytics'

urlpatterns = [

    path('', statistics_view, name='statistics'),
    path('raport/', report_form, name='report_form'),
    path('raport/generuj/', generate_excel_report, name='generate_excel_report'),

]
