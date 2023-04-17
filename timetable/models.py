import datetime

from django.db import models
from django.db.models import CASCADE

from users.models.users import User
from users.models.university import Auditorium, University_Building


class Type_TimetableItem(models.Model):
    name = models.CharField(max_length=60, blank=True)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TimetableItem(models.Model):
    name = models.CharField(max_length=60, blank=True)
    organazer = models.ForeignKey(User, on_delete=CASCADE, blank=True)
    type = models.ForeignKey(Type_TimetableItem, on_delete=CASCADE, blank=True)
    amount_people = models.IntegerField(blank=True, default=0)
    start_time = models.TimeField(auto_now=False, blank=True)
    end_time = models.TimeField(auto_now=False, blank=True)
    date = models.DateField(default=datetime.date(23, 1, 10))
    auditorium = models.ManyToManyField(Auditorium, blank=True)
    info = models.TextField()
    is_approved = models.BooleanField(default=False, null=True)
    who_approved = models.ForeignKey(User, on_delete=CASCADE, related_name='who_approved', null=True)
    datetime_approved = models.DateTimeField(auto_now=False, null=True)

    def __str__(self):
        return self.name
