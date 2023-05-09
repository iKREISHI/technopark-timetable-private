from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from timetable.models.timetable import TimetableItem


class UserReservationsList(LoginRequiredMixin, View):
    template_name = 'timetable/reservation/user/user-reservation-list.html'
    model = TimetableItem

    add_perm = 'timetable.add_timetableitem'
    view_perm = 'timetable.view_timetableitem'

    def get(self, request):
        user = request.user
        items = self.model.objects.filter(organazer=user)

        context = {
            'title': 'список моих заявок на бронирование аудиорий',
            'data': items,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        pass
