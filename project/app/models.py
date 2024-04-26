from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(
        max_length=255
    )
    slug = models.CharField(
        max_length=255,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class User(AbstractUser):
    middle_name = models.CharField(
        verbose_name='Отчество',
        max_length=255,
        blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name='users',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Report(models.Model):
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    address = models.CharField(
        max_length=255,
        null=True
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
