from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import UserRegisterForm, UserProfileForm

from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.scheduler.models import Task
from apps.observations.models import Observation

@login_required
def export_json(request):
    user = request.user

    zadania = list(Task.objects.filter(user=user).values(
        'plant__nazwa', 'typ__nazwa', 'data', 'opis', 'wykonane'
    ))
    obserwacje = list(Observation.objects.filter(user=user).values(
        'plant__nazwa', 'data', 'opis'
    ))

    data = {
        "zadania": zadania,
        "obserwacje": obserwacje
    }

    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = 'attachment; filename=dane.json'
    return response


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        return render(request, 'accounts/profile.html', {'profile': profile})


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self):
        # Возвращаем профиль текущего пользователя
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
