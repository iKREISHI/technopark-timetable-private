from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from users.models.university import Auditorium
from timetable.models.timetable import TimetableItem
from timetable.forms.reservation import ReservationAudienceForm
from datetime import date, timedelta, datetime
import locale
from timetable.forms.booking import BookingAuditoriumDate as BookingForm


class BookingTimeTableView(View, LoginRequiredMixin):
    template_name = 'timetable/booking/timetable-booking.html'
    model = TimetableItem
    form = ReservationAudienceForm

    def get(self, request, auditorium_id):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')

        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        days_of_week = []
        current_day = start_week
        # data = []

        while current_day <= end_week:
            day_info = {
                'value': current_day,
                'date': current_day.strftime("%d"),
                'month': current_day.strftime("%B").capitalize(),
                'weekday': current_day.strftime("%A").capitalize(),
                'date_serializtion': current_day.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            days_of_week.append(day_info)
            current_day += timedelta(days=1)

        data = self.model.objects.filter(auditorium=auditorium_id,  status='APPROVED').all().order_by('date', 'start_time', 'end_time')
        aud_name = Auditorium.objects.filter(id=auditorium_id,).first().name
        context = {
            'title': f'Забронировать аудиторию {aud_name}',
            'day_of_week': days_of_week,
            'timetable': data,
            'today': today,
            'auditorium_id': Auditorium.objects.filter(id=auditorium_id).first().id,
            'form': BookingForm,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')


class BookingTimeTableWeekView(View, LoginRequiredMixin):
    template_name = 'timetable/booking/timetable-booking.html'
    model = TimetableItem
    form = ReservationAudienceForm

    def get(self, request, auditorium_id, monday, sunday):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')

        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()
        today = date.today()
        start_week = mon
        end_week = sun
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

        data = self.model.objects.filter(auditorium=auditorium_id,  status='APPROVED').all().order_by('date', 'start_time', 'end_time')
        aud_name = Auditorium.objects.filter(id=auditorium_id,).first().name
        context = {
            'title':
                f'Забронировать аудиторию {aud_name} на '
                f'{start_week .strftime("%d")} {start_week .strftime("%B").capitalize()} '
                f'- {end_week .strftime("%d")} {end_week .strftime("%B").capitalize()} {end_week .strftime("%y")} года',
            'day_of_week': days_of_week,
            'timetable': data,
            'today': today,
            'auditorium_id': Auditorium.objects.filter(id=auditorium_id).first().id,
            'form': BookingForm,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')