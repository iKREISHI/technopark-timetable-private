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
    view_perm = 'timetable.view_timetableitem'

    def get(self, request):
        #if not request.user.has_perm(self.add_perm):
          #  raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm(self.add_perm):
            raise PermissionDenied

        form = self.form(request.POST)
        form.instance.organazer = request.user
        if form.is_valid():
            if request.user.is_superuser:
                form.instance.status = 'APPROVED'
                form.instance.who_approved = request.user
                form.instance.datetime_approved = timezone.now()
            form.save()
            return redirect('list-user-reservation')

        return render(request, self.template_name, self.context)