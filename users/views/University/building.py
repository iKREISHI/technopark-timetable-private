from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView
from users.forms.university import BuildingCreateForm
from users.models.university import University_Building


class AddUniversityBuilding(View):
    template_name = "university/add_item.html"
    context = {
        'title': 'Учебный корпус Университета',
        'form': BuildingCreateForm,
        'url_form': 'add-university-building',
    }

    def get(self, request):
        if not request.user.has_perm('users.add_university_building'):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        if not request.user.has_perm('users.add_university_building'):
            raise PermissionDenied
        form = BuildingCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-university-building')

        return render(request, self.template_name, self.context)


class ViewUniversityBuilding(View):
    template_name = 'university/university-building/view.html'
    model = University_Building
    context = {
        'title': 'Список Учебных корпусов',
        'data': model.objects.all()
    }

    def get(self, request):
        if not request.user.has_perm('users.add_university_building') and not request.user.has_perm('users.view_university_building'):
            raise PermissionDenied

        return render(request, self.template_name, self.context)

    def post(self, request):
        pass
