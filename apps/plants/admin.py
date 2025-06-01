from django.contrib import admin
from .models import Category, Plant

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'gatunek', 'user', 'data_dodania')
    list_filter = ('user', 'kategoria', 'oswietlenie')
    search_fields = ('nazwa', 'gatunek')
