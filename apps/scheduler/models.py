from django.db import models
from django.contrib.auth.models import User
from apps.plants.models import Plant

class TaskType(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = 'Typ zadania'
        verbose_name_plural = 'Typy zadań'

class Task(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='zadania')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zadania')
    typ = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    opis = models.TextField(blank=True, null=True)
    data = models.DateField()
    wykonane = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.typ} - {self.plant.nazwa} ({self.data})'

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'
        ordering = ['data']
