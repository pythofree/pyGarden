from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from apps.scheduler.models import Task
from django.contrib.auth.decorators import login_required

@login_required
def task_calendar_view(request):
    return render(request, 'scheduler/task_calendar.html')

@login_required
def calendar_events_json(request):
    user = request.user
    tasks = Task.objects.filter(user=user)

    events = []
    for task in tasks:
        events.append({
            'title': task.typ.nazwa if task.typ else 'Zadanie',
            'start': task.data.isoformat(),
            'color': '#198754' if task.wykonane else '#ffc107',
        })

    return JsonResponse(events, safe=False)
