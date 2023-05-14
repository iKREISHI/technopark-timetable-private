from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from users.models.users import User


# Name: list-admin-confirm-user
class UserConfirmation(View):
    template_name = 'user/confirm-admin.html'
    model = User

    add_perm = 'user.add_user'
    view_perm = 'user.view_user'
    change_perm = 'user.change_user'
    del_perm = 'user.delete_user'

    def get(self, request):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.change_perm):
            raise PermissionDenied

        items = self.model.objects.filter(is_verificated=False)

        context = {
            'title': 'Подтвердить нового пользователя',
            'data': items,
            'url_form': ''
        }

        return render(request, self.template_name, context)

    def post(self, request):
        pass


# Name: confirm-new-user
class ConfirmNewUser(View):
    add_perm = 'user.add_user'
    view_perm = 'user.view_user'
    change_perm = 'user.change_user'
    del_perm = 'user.delete_user'

    def get(self, request, user_id, str):
        if not request.user.has_perm(self.add_perm) and not request.user.has_perm(self.change_perm):
            raise PermissionDenied

        item = get_object_or_404(User, id=user_id)

        if str == 'APPROVED':
            item.is_verificated = True
        elif str == 'REJECTED':
            item.is_verificated = False
        else:
            item.is_verificated = False

        item.save()

        return redirect('list-admin-confirm-user')
