from django.contrib import admin
from timetable.models.timetable import Type_TimetableItem, TimetableItem
from .models.week import Week

admin.site.register(Type_TimetableItem)
admin.site.register(TimetableItem)
admin.site.register(Week)