from django.contrib import admin
from .models import Observation

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('plant', 'user', 'data')
    list_filter = ('plant', 'user', 'data')
    search_fields = ('plant__nazwa', 'user__username', 'opis')
