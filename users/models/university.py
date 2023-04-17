from django.db import models
from django.db.models import CASCADE


class University_Unit(models.Model):
    name = models.CharField(max_length=60, blank=True)
    abbreviation = models.CharField(max_length=10)
    info = models.TextField()

    def __str__(self):
        return self.name


class University_Building(models.Model):
    name = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=200)
    info = models.TextField()

    def __str__(self):
        return self.name


class Auditorium_Type(models.Model):
    name = models.CharField(max_length=60, blank=True)
    info = models.TextField()

    def __str__(self):
        return self.name


class Auditorium(models.Model):
    name = models.CharField(max_length=20, blank=True)
    building = models.ForeignKey(University_Building, on_delete=CASCADE)
    university_unit = models.ForeignKey(University_Unit, on_delete=CASCADE)
    type = models.ForeignKey(Auditorium_Type, on_delete=CASCADE)
    area = models.IntegerField(blank=True)
    capacity = models.IntegerField(blank=True)
    info = models.TextField()

    def __str__(self):
        return self.name
