from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from timetable.models.timetable import Type_TimetableItem, TimetableItem


class TimeTableItemTypeCreateForm(forms.ModelForm):
    class Meta:
        model = Type_TimetableItem
        fields = '__all__'


class TimeTableCreateForm(forms.ModelForm):

    class Meta:
        model = TimetableItem
        fields = ('name', 'organazer', 'type', 'auditorium', 'date', 'start_time', 'end_time', 'amount_people', 'info')