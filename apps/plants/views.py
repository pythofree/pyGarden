from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Plant
from .forms import PlantForm
from apps.scheduler.models import Task

class PlantListView(LoginRequiredMixin, ListView):
    model = Plant
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'
    paginate_by = 10

    def get_queryset(self):
        return Plant.objects.filter(user=self.request.user).order_by('-data_dodania')


class PlantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'
    context_object_name = 'plant'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()
        context['zadania'] = Task.objects.filter(plant=plant, user=self.request.user).order_by('data')
        return context


class PlantCreateView(LoginRequiredMixin, CreateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plants:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plants:list')

    def test_func(self):
        return self.get_object().user == self.request.user


class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Plant
    template_name = 'plants/plant_confirm_delete.html'
    success_url = reverse_lazy('plants:list')

    def test_func(self):
        return self.get_object().user == self.request.user


# ✅ Дополнительное представление: отметка задания как выполненного
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def mark_task_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.wykonane = True
    task.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
