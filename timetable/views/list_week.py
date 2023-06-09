from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium
from datetime import date, datetime, timedelta
from timetable.models.week import Week


class ListWeekView(View):
    template_name = 'timetable/Week/list-week.html'
    model = Week

    def get(self, request):
        Week.create_weeks_for_current_year()
        data = []
        today = date.today()
        for week in self.model.objects.all():
            el = {
                'start_day': week.start_day,
                'end_day': week.end_day,
                'monday': week.start_day.strftime('%d_%m_%y'),
                'sunday': week.end_day.strftime('%d_%m_%y'),
                'is_current_week': True if week.start_day.month == today.month or week.end_day.month == today.month else False,
                'is_last_week': True if week.start_day.month < today.month else False,
                'is_next_week': True if week.start_day.month > today.month else False,
            }
            data.append(el)

        context = {
            'title': 'Список недель',
            'weeks': data,
        }

        return render(request, self.template_name, context)

