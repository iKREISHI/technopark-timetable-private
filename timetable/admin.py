from django.contrib import admin
from timetable.models.timetable import Type_TimetableItem, TimetableItem
from .models.week import Week

Type_TimetableItem._meta.verbose_name = 'Тип мероприятия'
Type_TimetableItem._meta.verbose_name_plural = 'Типы мероприятия'

TimetableItem._meta.verbose_name = 'Мероприятие'
TimetableItem._meta.verbose_name_plural = 'Мероприятия'

Week._meta.verbose_name = 'Неделя'
Week._meta.verbose_name_plural = 'Недели'

admin.site.register(Type_TimetableItem)
admin.site.register(TimetableItem)
admin.site.register(Week)