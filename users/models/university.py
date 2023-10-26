from django.db import models
from django.db.models import CASCADE


class University_Unit(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name='Название подразделения')
    abbreviation = models.CharField(max_length=20, verbose_name='Аббревиатура подразделения')
    show_in_timetable = models.BooleanField(
        blank=False, null=True,
        verbose_name='Выводить в расписании',
        default=False
    )
    default_show = models.BooleanField(
        blank=False, null=True,
        default=False,
        verbose_name='Выводить автоматически в расписании',

    )
    info = models.TextField(verbose_name='Информация о подразделения')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.default_show:
            University_Unit.objects.exclude(pk=self.pk).update(default_show=False)
        super(University_Unit, self).save(*args, **kwargs)


class University_Building(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200)
    info = models.TextField()

    def __str__(self):
        return self.name


class Auditorium_Type(models.Model):
    name = models.CharField(max_length=100, blank=True)
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
