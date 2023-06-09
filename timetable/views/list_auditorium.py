from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium
from datetime import date, datetime, timedelta
from timetable.models.week import Week


class ListAuditoriumView(View):
    template_name = 'timetable/Week/list-auditorium.html'

    def get(self, request, monday, sunday):
        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()
        auditoriums = Auditorium.objects.all()

        context = {
            'title': 'Выберите аудиторию',
            'auditoriums': auditoriums,
            'monday': monday,
            'sunday': sunday,
        }

        return render(request, self.template_name, context)