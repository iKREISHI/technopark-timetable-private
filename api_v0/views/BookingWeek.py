from datetime import date, timedelta
from rest_framework import generics
from timetable.models.timetable import TimetableItem, Type_TimetableItem
from api_v0.serializers.TimetableItemSerializer import TimetableItemBaseInfoSerializer


class BookingCurrentWeekAPIView(generics.ListAPIView):
    serializer_class = TimetableItemBaseInfoSerializer

    def get_queryset(self):
        auditorium_id = self.kwargs['auditorium_id']

        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        queryset = TimetableItem.objects.filter(
            auditorium=auditorium_id,
            date__range=[start_week, end_week]
        ).all().order_by('date', 'start_time')

        return queryset