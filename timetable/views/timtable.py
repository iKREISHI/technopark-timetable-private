from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium, University_Unit
from datetime import date, timedelta, datetime
import locale


class ScheduleView(View):
    template_name = 'timetable/schedule/schedule.html'

    def get(self, request, monday, sunday):
        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()
        today = date.today()
        start_week = mon
        end_week = sun
        data = TimetableItem.objects.all().filter(status='APPROVED').order_by('date', 'start_time', 'end_time')
        auditoriums = Auditorium.objects.all()
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        days_of_week = []
        current_day = start_week
        # data = []

        while current_day <= end_week:
            day_info = {
                'value': current_day,
                'date': current_day.strftime("%d"),
                'month': current_day.strftime("%B").capitalize(),
                'weekday': current_day.strftime("%A").capitalize()
            }
            days_of_week.append(day_info)
            current_day += timedelta(days=1)

        context = {
            'title':
                f'Расписание на '
                f'{start_week .strftime("%d")} {start_week .strftime("%B").capitalize()} '
                f'- {end_week .strftime("%d")} {end_week .strftime("%B").capitalize()} {end_week .strftime("%y")} года',
            'day_of_week': days_of_week,
            'today': date.today(),
            'auditoriums': auditoriums,
            'monday': datetime.strftime(start_week, '%d_%m_%y'),
            'sunday': datetime.strftime(end_week, '%d_%m_%y'),
            'university_unit': University_Unit.objects.filter(show_in_timetable=True).all(),
            'timetable_items': data,
        }

        return render(request, self.template_name, context)


class CurrentScheduleView(View):
    template_name = 'timetable/schedule/schedule.html'

    def get(self, request):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        data = TimetableItem.objects.all().filter(status='APPROVED').order_by('date', 'start_time', 'end_time')
        auditoriums = Auditorium.objects.all()
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        days_of_week = []
        current_day = start_week
        # data = []

        while current_day <= end_week:
            day_info = {
                'value': current_day,
                'date': current_day.strftime("%d"),
                'month': current_day.strftime("%B").capitalize(),
                'weekday': current_day.strftime("%A").capitalize()
            }
            days_of_week.append(day_info)
            current_day += timedelta(days=1)

        context = {
            'title':
                f'Расписание на '
                f'{start_week .strftime("%d")} {start_week .strftime("%B").capitalize()} '
                f'- {end_week .strftime("%d")} {end_week .strftime("%B").capitalize()} {end_week .strftime("%y")} года',
            'day_of_week': days_of_week,
            'today': date.today(),
            'auditoriums': auditoriums,
            'monday': datetime.strftime(start_week, '%d_%m_%y'),
            'sunday': datetime.strftime(end_week, '%d_%m_%y'),
            'university_unit': University_Unit.objects.filter(show_in_timetable=True).all(),
            'timetable_items': data,
        }

        return render(request, self.template_name, context)