from django.shortcuts import render, redirect
from django.views import View


class ListWeekView(View):
    template_name = 'timetable/Week/list-week.html'

    def get(self, request):
        context = {
            'title': 'Открыть расписание',
        }
        return render(request, self.template_name, context)

