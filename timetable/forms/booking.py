from django import forms
from django.core.exceptions import ValidationError

from timetable.models.timetable import TimetableItem, Type_TimetableItem
import datetime
from users.models.university import Auditorium


class BookingAuditoriumDate(forms.ModelForm):
    name = forms.CharField(label='Название мероприятия или учебного занятия', max_length=60)

    start_time = forms.TimeField(
        label='Время начала',
        widget=forms.NumberInput(attrs={'type': 'time', 'min': '08:00', 'max': '22:00'})
    )
    end_time = forms.TimeField(
        label='Время окончания',
        widget=forms.NumberInput(attrs={'type': 'time', 'min': '08:00', 'max': '22:00'})
    )

    date = forms.DateField(widget=forms.HiddenInput)
    auditorium = forms.ModelMultipleChoiceField(
        queryset=Auditorium.objects.all(),
        widget=forms.HiddenInput,
    )
    amount_people = forms.IntegerField(label='Количество участников', min_value=0, max_value=300)
    type = forms.ModelChoiceField(
        label='Тип мероприятия',
        queryset=Type_TimetableItem.objects.all()
    )

    class Meta:
        model = TimetableItem
        fields = (
            'name', 'type', 'start_time', 'end_time', 'amount_people', 'info'
        )
        exclude = (
            'user',
        )