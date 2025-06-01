from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Plant
from .forms import PlantForm

class PlantListView(LoginRequiredMixin, ListView):
    """
    Список растений текущего пользователя.
    """
    model = Plant
    template_name = 'plants/plant_list.html'
    context_object_name = 'plants'
    paginate_by = 10

    def get_queryset(self):
        # Возвращаем только растения, принадлежащие текущему пользователю
        return Plant.objects.filter(user=self.request.user).order_by('-data_dodania')


class PlantDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Детальный просмотр конкретной Plant.
    """
    model = Plant
    template_name = 'plants/plant_detail.html'
    context_object_name = 'plant'

    def test_func(self):
        # Проверяем, что растение принадлежит текущему пользователю
        plant = self.get_object()
        return plant.user == self.request.user


class PlantCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового растения (Plant).
    """
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plants:list')

    def form_valid(self, form):
        # Устанавливаем user = текущий пользователь
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование существующего растения.
    """
    model = Plant
    form_class = PlantForm
    template_name = 'plants/plant_form.html'
    success_url = reverse_lazy('plants:list')

    def test_func(self):
        # Растение можно редактировать только если оно принадлежит текущему пользователю
        plant = self.get_object()
        return plant.user == self.request.user


class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление растения.
    """
    model = Plant
    template_name = 'plants/plant_confirm_delete.html'
    success_url = reverse_lazy('plants:list')

    def test_func(self):
        # Удалять можно только свои растения
        plant = self.get_object()
        return plant.user == self.request.user
