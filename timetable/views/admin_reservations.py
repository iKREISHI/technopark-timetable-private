from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from timetable.models.timetable import TimetableItem
from django.utils import timezone


class AdminApproveReservationList(LoginRequiredMixin, View):
    template_name = 'timetable/reservation/admin/reservation-list.html'
    model = TimetableItem

    add_perm = 'timetable.add_timetableitem'
    view_perm = 'timetable.view_timetableitem'
    change_perm = 'timetable.change_timetableitem'
    del_perm = 'timetable.delete_timetableitem'

    def get(self, request):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.change_perm):
            raise PermissionDenied

        items = self.model.objects.filter(status='PENDING')

        context = {
            'title': 'Одобрение заявок',
            'data': items,
            'url_form': ''
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class AdminApproveReservation(LoginRequiredMixin, View):
    model = TimetableItem
    add_perm = 'timetable.add_timetableitem'
    change_perm = 'timetable.change_timetableitem'

    def get(self, request, reservation_id, status):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.change_perm):
            raise PermissionDenied
        item = get_object_or_404(TimetableItem, id=reservation_id)
        # item = self.model.objects.get(id=reservation_id)
        item.status = status
        item.who_approved = request.user
        item.datetime_approved = timezone.now()
        item.save()
        return redirect('list-admin-reservation')

    def post(self, request):
        pass
