from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView
from users.forms.university import AuditoriumCreateForm, AuditoriumTypeCreateForm
from users.models.university import Auditorium, Auditorium_Type

add_perm = 'users.add_auditorium'
view_perm = 'users.view_auditorium'


class AddAuditorium(View):
    template_name = "university/add_item.html"
    context = {
        'title': 'UniversityUnitCreateForm',
        'form': AuditoriumCreateForm,
        'url_form': 'add-university-auditorium',
    }

    def get(self, request):
        if not request.user.has_perm(add_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm('users.add_university_unit'):
            raise PermissionDenied
        form = AuditoriumCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-university-auditorium')

        return render(request, self.template_name, self.context)


class ViewAuditorium(View):
    template_name = 'university/auditorium/view.html'
    model = Auditorium
    context = {
        'title': 'Список подразделений',
        'data': model.objects.all()
    }

    def get(self, request):
        if not request.user.has_perm(add_perm) and not request.user.has_perm(view_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        pass


class AddAuditoriumType(View):
    template_name = "university/add_item.html"
    context = {
        'title': 'Добавить тип аудитории',
        'form': AuditoriumTypeCreateForm,
        'url_form': 'add-university-auditorium-type',
    }
    add_perm = 'users.add_auditorium_type'
    view_perm = 'users.view_auditorium_type'

    def get(self, request):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.view_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm(self.add_perm):
            raise PermissionDenied
        form = AuditoriumTypeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-university-auditorium-type')
        return render(request, self.template_name, self.context)


class ViewAuditoriumType(View):
    template_name = 'university/auditorium/view-type.html'
    model = Auditorium_Type
    context = {
        'title': 'Список типов аудиторий',
        'data': model.objects.all(),
    }
    add_perm = 'users.add_auditorium_type'
    view_perm = 'users.view_auditorium_type'

    def get(self, request):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.view_perm):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        pass