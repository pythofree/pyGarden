from django.contrib import admin
from .models import TaskType, Task

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('nazwa',)
    search_fields = ('nazwa',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('typ', 'plant', 'user', 'data', 'wykonane')
    list_filter = ('typ', 'wykonane', 'data')
    search_fields = ('plant__nazwa', 'user__username')
