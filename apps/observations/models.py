from django.db import models
from django.contrib.auth.models import User
from apps.plants.models import Plant

class Observation(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='obserwacje')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='obserwacje')
    opis = models.TextField(blank=True, null=True)  # Описание наблюдения
    data = models.DateField(auto_now_add=True)      # Дата добавляется автоматически
    zdjecie = models.ImageField(upload_to='observations/%Y/%m/', blank=True, null=True)

    def __str__(self):
        return f'Obserwacja: {self.plant.nazwa} ({self.data})'

    class Meta:
        verbose_name = 'Obserwacja'
        verbose_name_plural = 'Obserwacje'
        ordering = ['-data']
