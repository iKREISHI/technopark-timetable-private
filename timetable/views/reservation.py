from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from timetable.models.timetable import TimetableItem
from timetable.forms.reservation import ReservationAudienceForm


class AddTimeTableReservation(LoginRequiredMixin, View):
    template_name = 'university/add_item.html'
    model = ...
    form = ReservationAudienceForm
    context = {
        'title': 'Забронировать аудиторию',
        'form': form,
        'url_form': 'add-user-reservation'
    }
    add_perm = 'timetable.add_timetableitem'
    change_perm = 'timetable.change_timetableitem'
    view_perm = 'timetable.view_timetableitem'

    def get(self, request):
        #if not request.user.has_perm(self.add_perm):
          #  raise PermissionDenied
        context = self.context
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')

        return render(request, self.template_name, context)

    def post(self, request):
        #if not request.user.has_perm(self.add_perm):
            #raise PermissionDenied
        context = self.context
        form = self.form(request.POST)
        form.instance.organazer = request.user
        if form.is_valid():
            if request.user.is_superuser or (
                    request.user.has_perm(self.add_perm) and request.user.has_perm(self.change_perm) and request.user.is_staff
            ):
                form.instance.status = 'APPROVED'
                form.instance.who_approved = request.user
                form.instance.datetime_approved = timezone.now()
            form.save()
            return redirect('list-user-reservation')
        context.update({'form': form})
        return render(request, self.template_name, context)
'''
            cleaned_data = form.cleaned_data
            auditorium = cleaned_data.get('auditorium')
            start_time = cleaned_data.get('start_time')
            end_time = cleaned_data.get('end_time')
            date = cleaned_data.get('date')

            if auditorium and date and start_time and end_time:
                # Check if any bookings exist for the selected auditorium, date, and time range
                bookings = TimetableItem.objects.filter(auditorium__in=auditorium, date=date, start_time__lt=end_time,
                                                        end_time__gt=start_time)
                if bookings.count() > 1:
                    form.add_error(None, 'На выбранное время найдено несколько бронирований.')
                    self.context['form'] = form
                    return render(request, self.template_name, self.context)
                elif bookings.exists():
                    # Handle the case when a single booking exists
                    booking = bookings.first()
                    form.add_error(None,
                                   f'Аудитория уже забронирован на выбранное время ({booking.start_time} - {booking.end_time}).')
                    self.context['form'] = form
                    return render(request, self.template_name, self.context)'''
