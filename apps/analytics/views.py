from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now
from django.utils.dateparse import parse_date
from datetime import timedelta
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font
from apps.plants.models import Plant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.scheduler.models import Task
from apps.observations.models import Observation





@login_required
def statistics_view(request):
    user = request.user
    today = now().date()
    date_from = today - timedelta(days=30)

    tasks = Task.objects.filter(user=user, data__range=(date_from, today)).select_related('typ')
    tasks_done = tasks.filter(wykonane=True)
    tasks_pending = tasks.filter(wykonane=False).count()
    observations = Observation.objects.filter(user=user, data__range=(date_from, today))

    watering_map = defaultdict(int)
    fertilizing_map = defaultdict(int)
    repotting_map = defaultdict(int)
    observation_map = defaultdict(int)

    for task in tasks_done:
        date_str = task.data.strftime('%Y-%m-%d')
        typ_name = task.typ.nazwa.lower() if task.typ else ''
        if 'podlew' in typ_name:
            watering_map[date_str] += 1
        elif 'nawoż' in typ_name:
            fertilizing_map[date_str] += 1
        elif 'przesadz' in typ_name:
            repotting_map[date_str] += 1

    for obs in observations:
        date_str = obs.data.strftime('%Y-%m-%d')
        observation_map[date_str] += 1

    chart_labels = []
    chart_watering = []
    chart_fertilizing = []
    chart_repotting = []
    chart_observations = []

    for i in range(31):
        day = date_from + timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        chart_labels.append(day_str)
        chart_watering.append(watering_map.get(day_str, 0))
        chart_fertilizing.append(fertilizing_map.get(day_str, 0))
        chart_repotting.append(repotting_map.get(day_str, 0))
        chart_observations.append(observation_map.get(day_str, 0))

    context = {
        'done_tasks': tasks_done.count(),
        'pending_tasks': tasks_pending,
        'obs_count': observations.count(),
        'chart_labels': chart_labels,
        'chart_watering': chart_watering,
        'chart_fertilizing': chart_fertilizing,
        'chart_repotting': chart_repotting,
        'chart_observations': chart_observations,
    }
    return render(request, 'analytics/statistics.html', context)


@login_required
def report_form(request):
    plants = Plant.objects.filter(user=request.user)
    return render(request, 'analytics/report_form.html', {'plants': plants})


@login_required
def generate_excel_report(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('plants')
        date_from = parse_date(request.POST.get('date_from'))
        date_to = parse_date(request.POST.get('date_to'))

        wb = Workbook()
        ws = wb.active
        ws.title = "Raport"

        ws.append([
            'Roślina', 'Typ zadania', 'Data zadania', 'Wykonane',
            'Opis zadania', 'Opis obserwacji', 'Data obserwacji'
        ])
        for cell in ws["1:1"]:
            cell.font = Font(bold=True)

        for plant in Plant.objects.filter(id__in=selected_ids, user=request.user):
            tasks = Task.objects.filter(plant=plant, data__range=(date_from, date_to))
            observations = Observation.objects.filter(plant=plant, data__range=(date_from, date_to))

            for task in tasks:
                ws.append([
                    plant.nazwa,
                    task.typ.nazwa if task.typ else '',
                    task.data.strftime('%Y-%m-%d'),
                    'Tak' if task.wykonane else 'Nie',
                    task.opis or '',
                    '', ''
                ])

            for obs in observations:
                ws.append([
                    plant.nazwa,
                    '', '', '', '',
                    obs.opis or '',
                    obs.data.strftime('%Y-%m-%d')
                ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=raport.xlsx'
        wb.save(response)
        return response
