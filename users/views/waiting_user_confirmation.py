from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from users.models.users import User


# Name: waiting-user-confirm
class WaitingUserConfirm(View):
    template_name = 'user/waiting-user-confirmations.html'
    context = {
        'title': 'Ожидание подтверждения',
    }

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        pass