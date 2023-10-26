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

        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        week_data = {
            'start_week': start_week,
            'end_week': end_week,
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
            'end_week': datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date(),
        }

        data = {
            **week_data,
            'results': serializer.data,
        }

        return Response(data)


class BookingCurrentWeekMinimalAPIView(BookingCurrentWeekAPIView):
    serializer_class = BookingSerialazer

    def get_queryset(self):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        queryset = TimetableItem.objects.filter(
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        week_data = {
            'start_week': start_week,
            'end_week': end_week,
        }

        data = {
            **week_data,
            'results': serializer.data,
        }

        return Response(data)

# BookingByUniversityUnitListAPIView
class BookingByUUListAPIView(BookingWeekMinimalAPIView):
    serializer_class = BookingSerialazer

    def get_queryset(self):
        id_university_unit = self.kwargs['id_university_unit']
        start_week = datetime.strptime(self.kwargs['monday'], '%d_%m_%y').date()
        end_week = datetime.strptime(self.kwargs['sunday'], '%d_%m_%y').date()
        queryset = TimetableItem.objects.filter(
            auditorium__university_unit_id=id_university_unit,
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset


# BookingByUniversityUnitListAPIView
class BookingByUUCurrentWeekListAPIView(BookingCurrentWeekMinimalAPIView):
    serializer_class = BookingSerialazer

    def get_queryset(self):
        id_university_unit = int(self.kwargs['id_university_unit'])
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        queryset = TimetableItem.objects.filter(
            auditorium__university_unit_id=id_university_unit,
            date__range=[start_week, end_week],
            status='APPROVED',
        ).all().order_by('date', 'start_time')

        return queryset
