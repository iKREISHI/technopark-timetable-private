from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from django.views.generic import ListView
from users.models.users import User
from users.forms.profile_edit import UserProfileEditForm


class ProfileView(View, LoginRequiredMixin):
    template_name = 'user/profile.html'

    def get(self, request):
        user = request.user

        context = {
            'title': 'Информация о пользователе',
            'user': user,
            'form': UserProfileEditForm,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user

        form = UserProfileEditForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user-profile')

        context = {
            'title': 'Информация о пользователе',
            'user': user,
            'form': UserProfileEditForm,
        }

        return render(request, self.template_name, context)



class EditProfileView(View, LoginRequiredMixin):
    template_name = ''

    def get(self, request):
        pass

    def post(self, request):
        pass