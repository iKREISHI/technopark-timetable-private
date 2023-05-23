from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from timetable.models.timetable import TimetableItem
import datetime


class UserReservationsList(LoginRequiredMixin, View):
    template_name = 'timetable/reservation/user/user-reservation-list.html'
    model = TimetableItem

    add_perm = 'timetable.add_timetableitem'
    view_perm = 'timetable.view_timetableitem'

    def get(self, request):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')
        items = self.model.objects.filter(organazer=request.user)
        context = {
            'title': 'список моих заявок на бронирование аудиорий',
            'data': items,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


# name: update-user-reservation
class UserReservationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'timetable/item/update_view.html'
    model = TimetableItem

    fields = [
        'name',
        'type',
        'amount_people',
        'auditorium',
        'date',
        'start_time',
        'end_time',
        'info',
    ]

    extra_context = {
        'title': '',
        'url_redirect': '',
    }

    def get_success_url(self):
        return reverse('list-user-reservation')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(organazer=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.organazer == self.request.user:
            raise Http404("Вы не имеете доступа к этой заявке.")
        return obj

    def get(self, request, *args, **kwargs):
        if not request.user.is_verificated:
            return redirect('waiting-user-confirm')
        self.object = self.get_object()
        self.extra_context.update({'title': f'Редактировать заявку: {self.object.name}'})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')
        date = form.cleaned_data.get('date')
        amount_people = form.cleaned_data.get('amount_people')

        if start_time and end_time and start_time >= end_time:
            form.add_error('end_time', 'Время окончания должно быть позже времени начала.')

        if date and date < datetime.date.today():
            form.add_error('date', 'Нельзя выбрать прошедшую дату.')

        if amount_people and amount_people < 0:
            form.add_error('amount_people', 'Количество людей должно быть положительным числом.')

        if form.errors:
            return self.form_invalid(form)

        return super().form_valid(form)