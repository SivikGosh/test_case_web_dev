from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True)

    def __srt__(self):
        return f'{self.first_name}[0]. {self.middle_name}[0]. {self.last_name}'

    class Meta:
        verbose_name = 'Отчество'
