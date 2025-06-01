from django import forms
from .models import Observation

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['plant', 'opis', 'zdjecie']
        widgets = {
            'opis': forms.Textarea(attrs={'rows': 4}),
        }
