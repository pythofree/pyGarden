from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from utils.weather import get_weather
from .models import Task
from .forms import TaskForm
from django.utils.timezone import now
from datetime import datetime

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'scheduler/task_list.html'
    context_object_name = 'zadania'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('data')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context['zadania']
        today = now().date()

        city = getattr(self.request.user.profile, 'city', None)
        weather = get_weather(city) if city else None
        context['weather'] = weather

        for task in tasks:
            task.skip_reason = None
            if task.data != today:
                continue
            if not (weather and task.typ and hasattr(task.typ, 'nazwa')):
                continue
            typ_nazwa = task.typ.nazwa.strip().lower()
            if typ_nazwa == "podlewanie":
                if weather.get("is_rainy") is True:
                    task.skip_reason = "🌧️ Odroczone z powodu deszczu"
                elif weather.get("humidity", 0) >= 85:
                    task.skip_reason = "💧 Odroczone: wysoka wilgotność"

        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('tasks:calendar')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
        return self.get_object().user == self.request.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'scheduler/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:list')

    def test_func(self):
        return self.get_object().user == self.request.user

def mark_done(request, pk):
    task = Task.objects.get(pk=pk)
    if task.user == request.user:
        task.wykonane = True
        task.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def task_list_for_day_view(request, date):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return redirect('tasks:list')

    tasks = Task.objects.filter(user=request.user, data=date_obj).order_by('data')
    city = getattr(request.user.profile, 'city', None)
    weather = get_weather(city) if city else None

    return render(request, 'scheduler/task_list.html', {
        'zadania': tasks,
        'weather': weather,
        'selected_date': date_obj,
    })
