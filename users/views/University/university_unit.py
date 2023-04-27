from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView
from users.forms.university import UniversityUnitCreateForm
from users.models.university import University_Unit


class AddUniversityUnit(View):
    template_name = "university/add_item.html"
    context = {
        'title': 'UniversityUnitCreateForm',
        'form': UniversityUnitCreateForm,
        'url_form': 'add-university-unit',
    }

    def get(self, request):
        if not request.user.has_perm('users.add_university_unit'):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm('users.add_university_unit'):
            raise PermissionDenied
        form = UniversityUnitCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-university-unit')

        return render(request, self.template_name, self.context)


class ViewUniversityUnit(View):
    template_name = 'university/university-unit/view.html'
    model = University_Unit
    context = {
        'title': 'Список подразделений',
        'data': model.objects.all()
    }

    def get(self, request):
        if not request.user.has_perm('users.add_university_unit') and not request.user.has_perm('users.view_university_unit'):
            raise PermissionDenied

        return render(request, self.template_name, self.context)


    def post(self, request):
        pass
