from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE
from users.models.university import University_Unit


class User(AbstractUser):
    patronymic = models.CharField(max_length=100, verbose_name='Отчетсво', blank=True)
    university_unit = models.ForeignKey(University_Unit, on_delete=CASCADE, null=True, blank=True, verbose_name='Подразделение Университета')
    phone_number = models.CharField(max_length=17, null=True, blank=True, verbose_name='Номер телефона')
    is_verificated = models.BooleanField(default=False, blank=True)
    info = models.TextField(verbose_name='Дополнительная информация')

    def __str__(self):
        return self.username




