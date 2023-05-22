from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium
from datetime import datetime


class TimetableWeekView(View):
    template_name = 'timetable/schedule/week.html'

    def get(self, request, monday, sunday):
        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()

        auditoriums = Auditorium.objects.all()
        context = {
            'title': f'Расписание на неделю '
                     f'{monday} '
                     f'- {sunday}',
            'auditoriums': auditoriums,
            'start_week': mon,
            'end_week': sun,
        }
        return render(request, self.template_name, context)