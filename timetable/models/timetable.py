import datetime

from django.db import models
from django.db.models import CASCADE

from users.models.users import User
from users.models.university import Auditorium


class Type_TimetableItem(models.Model):
    name = models.CharField(max_length=60, blank=True)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TimetableItem(models.Model):
    name = models.CharField(max_length=60, blank=True, verbose_name='Название')
    organazer = models.ForeignKey(User, on_delete=CASCADE, blank=True, verbose_name='Ответсвенный')
    type = models.ForeignKey(Type_TimetableItem, on_delete=CASCADE, blank=False, null=True, verbose_name='Тип мероприятия')
    amount_people = models.IntegerField(blank=True, default=0, verbose_name='Количество человек')
    start_time = models.TimeField(auto_now=False, blank=True, verbose_name='Время начала')
    end_time = models.TimeField(auto_now=False, blank=True, verbose_name='Время окончания')
    date = models.DateField(default=datetime.date(23, 1, 10), verbose_name='Дата')
    auditorium = models.ManyToManyField(Auditorium, blank=True, verbose_name='Аудитория')
    info = models.TextField(verbose_name='Дополнительная информация')
    # is_approved = models.BooleanField(default=False, null=True, verbose_name='Одобренно')
    STATUS_CHOICES = (
        ('PENDING', 'Ожидает одобрения'),
        ('APPROVED', 'Одобрено'),
        ('REJECTED', 'Отклонено'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name='Статус заявки')
    who_approved = models.ForeignKey(User, on_delete=CASCADE, related_name='who_approved', null=True, verbose_name='Кто одобрил')
    datetime_approved = models.DateTimeField(auto_now=False, null=True, verbose_name='Дата одобрения')

    def __str__(self):
        return self.name
