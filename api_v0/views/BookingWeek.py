from datetime import date, timedelta
from rest_framework import generics
from rest_framework.response import Response

from timetable.models.timetable import TimetableItem, Type_TimetableItem
from users.models.university import Auditorium
from api_v0.serializers.TimetableItemSerializer import (
    TimetableItemBaseInfoSerializer, TimetableAuditoriumReservationSerializer,
    BookingSerialazer
)
from datetime import datetime


class BookingCurrentWeekAPIView(generics.ListAPIView):
    serializer_class = TimetableItemBaseInfoSerializer

    def get_queryset(self):
        auditorium_id = self.kwargs['auditorium_id']

        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        queryset = TimetableItem.objects.filter(
            auditorium=auditorium_id,
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        week_data = {
            'start_week': datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date(),
            'end_week': datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date(),
        }

        data = {
            **week_data,
            'results': serializer.data,
        }

        return Response(data)


class BookingWeekAPIView(generics.ListAPIView):
    serializer_class = TimetableItemBaseInfoSerializer

    def get_queryset(self):
        # auditorium_id = self.kwargs['auditorium_id']
        start_week = datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date()
        end_week = datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date()

        queryset = TimetableItem.objects.filter(
            # auditorium=auditorium_id,
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        week_data = {
            'start_week': datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date(),
            'end_week': datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date(),
        }

        data = {
            **week_data,
            'results': serializer.data,
        }

        return Response(data)


class BookingWeekMinimalAPIView(generics.ListAPIView):
    serializer_class = BookingSerialazer

    def get_queryset(self):
        start_week = datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date()
        end_week = datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date()

        queryset = TimetableItem.objects.filter(
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        week_data = {
            'start_week': datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date(),
            'end_week':   datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date(),
        }

        data = {
            **week_data,
            'results': serializer.data,
        }

        return Response(data)


class BookingByWeekAPIView(generics.ListAPIView):
    serializer_class = TimetableAuditoriumReservationSerializer

    def get_queryset(self):
        start_week = datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date()
        end_week = datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date()

        items = TimetableItem.objects.filter(
            date__range=[start_week, end_week]
        ).all().order_by('date', 'start_time')



        queryset = Auditorium.objects.all().timetableitem_set.filter(
            date__range=[start_week, end_week]
        )

        return queryset
