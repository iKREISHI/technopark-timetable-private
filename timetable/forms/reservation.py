from django import forms
from django.core.exceptions import ValidationError

from timetable.models.timetable import TimetableItem, Type_TimetableItem
import datetime
from users.models.university import Auditorium


class ReservationAudienceForm(forms.ModelForm):
    name = forms.CharField(label='Название мероприятия или учебного занятия', max_length=60)
    date = forms.DateField(label='Дата мероприятия', initial=datetime.date.today(),
                           widget=forms.SelectDateWidget(attrs={}))
    start_time = forms.TimeField(
        label='Время начала',
        widget=forms.NumberInput(attrs={'type': 'time', 'min': '08:00', 'max': '22:00'})
    )
    end_time = forms.TimeField(
        label='Время окончания',
        widget=forms.NumberInput(attrs={'type': 'time', 'min': '08:00', 'max': '22:00'})
    )
    auditorium = forms.ModelMultipleChoiceField(
        label='Аудитория',
        queryset=Auditorium.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    amount_people = forms.IntegerField(label='Количество участников', min_value=0, max_value=300)
    type = forms.ModelChoiceField(
        label='Тип мероприятия',
        queryset=Type_TimetableItem.objects.all()
    )

    class Meta:
        model = TimetableItem
        fields = (
            'name', 'type', 'date', 'start_time', 'end_time', 'auditorium', 'amount_people'
        )
        exclude = (
            'user',
        )

'''
    def clean(self):
        cleaned_data = super().clean()
        auditorium = cleaned_data.get('auditorium')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')
        if auditorium and date and start_time and end_time:
            # Проверяем, занята ли аудитория на выбранные дату и время
            bookings = TimetableItem.objects.filter(auditorium=auditorium, date=date)
            for booking in bookings:
                # Проверяем, пересекается ли забронированное время с выбранным
                if booking.start_time < end_time and start_time < booking.end_time:
                    raise forms.ValidationError(
                        f'Аудитория уже занята на выбранное время ({booking.start_time} - {booking.end_time})')
                        
'''