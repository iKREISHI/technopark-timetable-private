from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView
from timetable.forms.timetable_item import TimeTableItemTypeCreateForm, TimeTableCreateForm
from timetable.models.timetable import Type_TimetableItem, TimetableItem


class AddTimeTableItemType(View):
    # template_name = 'timetable/item/add_item.html'
    template_name = 'university/add_item.html'
    add_perm = 'timetable.add_type_timetableitem'
    view_perm = 'timetable.view_type_timetableitem'
    context = {
        'title': 'Добавить тип мероприятия',
        'form': TimeTableItemTypeCreateForm,
        'url_form': 'add-timetable-item-type'
    }

    def get(self, request):
        if not request.user.has_perm(self.add_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm(self.add_perm):
            raise PermissionDenied
        form = TimeTableItemTypeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-timetable-item-type')
        return render(request, self.template_name, self.context)


class ViewTimeTableItemType(View):
    template_name = 'timetable/item/view_item.html'
    add_perm = 'timetable.add_type_timetableitem'
    view_perm = 'timetable.view_type_timetableitem'
    model = Type_TimetableItem
    context = {
        'title': 'Добавить тип мероприятия',
        'data': model.objects.all()
    }

    def get(self, request):
        if not request.user.has_perm(self.view_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        pass
