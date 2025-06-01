from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'nazwa',
            'gatunek',
            'kategoria',
            'zdjecie',
            'ostatnie_podlanie',
            'interwal_podlania',
            'interwal_nawozenia',
            'interwal_przesadzania',
            'oswietlenie',
            'ph_min',
            'ph_max',
            'uwagi',
        ]
        widgets = {
            'ostatnie_podlanie': forms.DateInput(attrs={'type': 'date'}),
        }
