from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from timetable.models.timetable import TimetableItem


class TimeTableItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TimetableItem
    template_name = 'timetable/item/delete_view.html'
    success_url = reverse_lazy('timetable:item_list')  # Укажите URL-адрес для перенаправления после успешного удаления объекта

    def test_func(self):
        # Проверка, что пользователь является владельцем заявки или администратором
        item = self.get_object()
        return self.request.user == item.user or self.request.user.is_superuser

    def handle_no_permission(self):
        # Обработка случая, когда пользователь не является владельцем заявки или администратором
        return HttpResponseRedirect("/")

    def delete(self, request, *args, **kwargs):
        # Переопределение метода delete() для выполнения дополнительной логики перед удалением объекта
        self.object = self.get_object()
        # Добавьте здесь дополнительную логику, если требуется
        return super().delete(request, *args, **kwargs)
