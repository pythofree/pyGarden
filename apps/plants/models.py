from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # Поле «nazwa» (название категории) должно быть уникальным
    nazwa = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Plant(models.Model):
    # Варианты требований к освещению (по-польски)
    LIGHT_CHOICES = [
        ('low', 'Niskie'),
        ('medium', 'Średnie'),
        ('high', 'Wysokie'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')
    nazwa = models.CharField(max_length=255)                   # название растения
    gatunek = models.CharField(max_length=255, blank=True)     # «gatunek» = вид (опционально)
    kategoria = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )                                                         # категория (связь «многие-ко-многим» упрощена)
    zdjecie = models.ImageField(upload_to='plants/%Y/%m/', blank=True, null=True)
    data_dodania = models.DateField(auto_now_add=True)         # дата добавления (автоматически)
    ostatnie_podlanie = models.DateField(null=True, blank=True)  # дата последнего полива
    interwal_podlania = models.PositiveIntegerField(
        default=7,
        help_text='Interwał (w dniach) między podlaniami'
    )
    interwal_nawozenia = models.PositiveIntegerField(
        default=30,
        help_text='Interwał (w dniach) na nawożenie'
    )
    interwal_przesadzania = models.PositiveIntegerField(
        default=365,
        help_text='Interwał (w dniach) na przesadzanie'
    )
    oswietlenie = models.CharField(
        max_length=10,
        choices=LIGHT_CHOICES,
        default='medium'
    )
    ph_min = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    ph_max = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    uwagi = models.TextField(blank=True, null=True)            # заметки/комментарии

    def __str__(self):
        return f'{self.nazwa} ({self.gatunek})'

    class Meta:
        verbose_name = 'Roślina'
        verbose_name_plural = 'Rośliny'
