from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Observation
from .forms import ObservationForm

class ObservationListView(LoginRequiredMixin, ListView):
    model = Observation
    template_name = 'observations/observation_list.html'
    context_object_name = 'obserwacje'
    paginate_by = 10

    def get_queryset(self):
        return Observation.objects.filter(user=self.request.user).order_by('-data')


class ObservationCreateView(LoginRequiredMixin, CreateView):
    model = Observation
    form_class = ObservationForm
    template_name = 'observations/observation_form.html'
    success_url = reverse_lazy('observations:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ObservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Observation
    form_class = ObservationForm
    template_name = 'observations/observation_form.html'
    success_url = reverse_lazy('observations:list')

    def test_func(self):
        observation = self.get_object()
        return observation.user == self.request.user


class ObservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Observation
    template_name = 'observations/observation_confirm_delete.html'
    success_url = reverse_lazy('observations:list')

    def test_func(self):
        observation = self.get_object()
        return observation.user == self.request.user
