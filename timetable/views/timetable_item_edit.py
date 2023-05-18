from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from timetable.models.timetable import TimetableItem
from timetable.forms.reservation import ReservationAudienceForm
import datetime


class TimeTableItemUpdateView(LoginRequiredMixin, UpdateView):
    model = TimetableItem
    template_name = 'timetable/item/update_view.html'

    fields = [
        'name',
        'type',
        'amount_people',
        'auditorium',
        'date',
        'start_time',
        'end_time',
        'status',
        'info',
    ]

    extra_context = {
        'title': 'test',
        'url_redirect': '',
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser or not (
          request.user.is_staff
          and request.user.has_perm('timetable.add_timetableitem')
          and request.user.has_perm('timetable.change_timetableitem')
          and request.user.has_perm('timetable.view_timetableitem')
          and request.user.has_perm('timetable.delete_timetableitem')
        ):
            return HttpResponseRedirect("/")
        self.object = self.get_object()
        self.extra_context.update({'title': f'Редактировать заявку: {self.object.name}'})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Дополнительная валидация формы
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')
        date = form.cleaned_data.get('date')
        amount_people = form.cleaned_data.get('amount_people')

        if start_time and end_time and start_time >= end_time:
            form.add_error('end_time', 'Время окончания должно быть позже времени начала.')

        if date and date < datetime.date.today():
            form.add_error('date', 'Нельзя выбрать прошедшую дату.')

        if amount_people and amount_people < 0:
            form.add_error('amount_people', 'Количество людей должно быть положительным числом.')

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)