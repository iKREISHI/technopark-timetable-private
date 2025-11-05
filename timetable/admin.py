from django.contrib import admin
from timetable.models.timetable import Type_TimetableItem, TimetableItem


class TimetableItemAdminPanel(admin.ModelAdmin):
    list_display = (
        'name', 'organazer', 'type', 'date', 'start_time', 'end_time', 'amount_people'
    )
    search_fields = (
        'name', 'organazer', 'type', 'date', 'start_time', 'end_time', 'auditorium',
    )


class TypeTimetableItemAdminPanel(admin.ModelAdmin):
    list_display = (
        'name', 'info',
    )
    search_fields = (
        'name',
    )


class WeekAdminPanel(admin.ModelAdmin):
    list_display = (
        'start_day', 'end_day'
    )
    search_fields = (
        'start_day', 'end_day'
    )

Type_TimetableItem._meta.verbose_name = 'Тип мероприятия'
Type_TimetableItem._meta.verbose_name_plural = 'Типы мероприятия'

TimetableItem._meta.verbose_name = 'Мероприятие'
TimetableItem._meta.verbose_name_plural = 'Мероприятия'

admin.site.register(Type_TimetableItem, TypeTimetableItemAdminPanel)
admin.site.register(TimetableItem, TimetableItemAdminPanel)