from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField('Отчество', max_length=255, blank=True)

    def __srt__(self):
        return f'{self.first_name}. {self.middle_name}. {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
