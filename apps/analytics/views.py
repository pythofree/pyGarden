from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.scheduler.models import Task
from apps.observations.models import Observation
from django.utils.timezone import now
from datetime import timedelta

@login_required
def statistics_view(request):
    user = request.user

    # Кол-во задач за последние 30 дней
    last_30_days = now().date() - timedelta(days=30)
    recent_tasks = Task.objects.filter(user=user, data__gte=last_30_days)
    tasks_done = recent_tasks.filter(wykonane=True).count()
    tasks_pending = recent_tasks.filter(wykonane=False).count()

    # Кол-во наблюдений за последние 30 дней
    recent_observations = Observation.objects.filter(user=user, data__gte=last_30_days).count()

    context = {
        'tasks_done': tasks_done,
        'tasks_pending': tasks_pending,
        'recent_observations': recent_observations,
    }

    return render(request, 'analytics/statistics.html', context)
