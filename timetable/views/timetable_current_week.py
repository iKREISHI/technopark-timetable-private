from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium
from datetime import date, timedelta


class TimeTableCurrentWeekView(View):
    template_name = 'timetable/schedule/current_week.html'
    model = TimetableItem

    def get(self, request):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        auditoriums = Auditorium.objects.all()
        '''data = self.model.objects\
            .filter(date__range=[start_week, end_week], status='APPROVED', auditorium__in=auditoriums)\
            .order_by('date', 'start_time', 'end_time')'''

        context = {
            'title': 'Расписание на текущую неделю',
            'auditoriums': auditoriums,
            'start_week': start_week,
            'end_week': end_week,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class TimeTableCurrentWeekListView(ListView):
    template_name = 'timetable/schedule/current_week.html'
    model = TimetableItem
    extra_context = {
        'title': 'Расписание на текущую неделю',
        'auditoriums': Auditorium.objects.all(),
    }