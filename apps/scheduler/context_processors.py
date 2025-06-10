from datetime import date
from apps.scheduler.models import Task

def todays_tasks(request):
    if request.user.is_authenticated:
        tasks_today = Task.objects.filter(
            user=request.user,
            data=date.today(),
            wykonane=False
        ).select_related('typ', 'plant')
    else:
        tasks_today = []

    return {'tasks_today': tasks_today}
