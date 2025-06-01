from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone', 'preferred_units', 'notifications_enabled', 'city')
    search_fields = ('user__username', 'user__email', 'city')

