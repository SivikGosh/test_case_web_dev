from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f'{self.first_name[0]}. {self.middle_name[0]}. {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Report(models.Model):
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    date = models.DateField()
    income = models.DecimalField(
        verbose_name='Выручка',
        max_digits=7,
        decimal_places=2
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
