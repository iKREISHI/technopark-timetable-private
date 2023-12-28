from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import json
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from timetable.models.timetable import TimetableItem
from users.models.university import Auditorium, University_Unit
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
            'auditoriums': auditoriums.order_by("name"),
            'university_unit': University_Unit.objects.filter(show_in_timetable=True).all(),
            'today': date.today(),
            'start_week': start_week,
            'end_week': end_week,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class TimeTableCurrentWeekJSONView(View):
    template_name = 'timetable/schedule/current_week.html'
    model = TimetableItem

    def get(self, request):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        auditoriums = Auditorium.objects.all()
        data = []

        for aud in auditoriums:
            timetable_items = aud.timetableitem_set.filter(date__range=[start_week, end_week]).order_by('date',
                                                                                                        'start_time')
            items = []

            for item in timetable_items:
                if item.organazer.last_name and item.organazer.first_name:
                    responsible = f"{item.organazer.last_name} {item.organazer.first_name}"
                else:
                    responsible = f"Пользователь: {item.organazer}"

                items.append({
                    'date': item.date,
                    'start_time': item.start_time.strftime('%H:%M'),
                    'end_time': item.end_time.strftime('%H:%M'),
                    'name': item.name,
                    'responsible': responsible
                })

            data.append({
                'name': aud.name,
                'items': items
            })

        context = {
            'title': 'Расписание на текущую неделю',
            'data': data
        }

        json_data = json.dumps(context)
        return HttpResponse(json_data, content_type='application/json')
