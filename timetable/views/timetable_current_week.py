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
        context = {
            'title': f'Расписание на текущую неделю',
            'auditoriums': auditoriums,
            'start_week': start_week,
            'end_week': end_week,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
