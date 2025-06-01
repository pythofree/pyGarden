from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['plant', 'typ', 'opis', 'data', 'wykonane']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
