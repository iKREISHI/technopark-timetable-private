from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, serializers
from rest_framework.permissions import IsAuthenticated
from timetable.models.timetable import TimetableItem, Type_TimetableItem
from api_v0.serializers.TimetableItemSerializer import (
    TimetableItemSerializer,
    TimetableReservationSerializer
)
from timetable.forms.booking import BookingAuditoriumDate
from users.models.university import Auditorium
import datetime

class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = TimetableItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    add_perm = 'timetable.add_timetableitem'
    change_perm = 'timetable.change_timetableitem'
    view_perm = 'timetable.view_timetableitem'

    def perform_create(self, serializer):
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        date = serializer.validated_data['date']
        auditorium = self.request.data.get('auditorium')
        amount = serializer.validated_data['amount_people']

        if date < datetime.date.today():
            raise serializers.ValidationError(
                f'Невозможно забронировать аудиторию на прошедшую дату'
            )
        if amount > Auditorium.objects.filter(id=auditorium).first().capacity:
            raise serializers.ValidationError(
                f'Аудитория {Auditorium.objects.filter(id=auditorium).first()} не может вместить {amount} человек')

        # Проверка наличия уже существующих бронирований на данное время и дату
        existing_bookings = serializer.Meta.model.objects.filter(
            date=date,
            auditorium=auditorium,
            start_time__lte=end_time,
            end_time__gte=start_time,
            status='APPROVED',
        )
        if existing_bookings.exists():
            raise serializers.ValidationError(f'Аудитория {Auditorium.objects.filter(id=auditorium).first()} занята на выбранное время и дата. Выберите другое время.')

        if self.request.user.is_superuser or (
                self.request.user.has_perm(self.add_perm)
                and self.request.user.has_perm(self.change_perm)
                and self.request.user.is_staff
        ):
            serializer.save(
                organazer=self.request.user,
                auditorium=auditorium,
                status='APPROVED',
                who_approved=self.request.user,
                datetime_approved=timezone.now()
            )
        else:
            serializer.save(
                organazer=self.request.user,
                auditorium=auditorium,
            )


class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = TimetableReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    add_perm = 'timetable.add_timetableitem'
    change_perm = 'timetable.change_timetableitem'
    view_perm = 'timetable.view_timetableitem'

    def perform_create(self, serializer):
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        date = serializer.validated_data['date']
        auditoriums = serializer.validated_data['auditoriums']
        print(auditoriums)

        for auditorium in auditoriums:
            existing_bookings = serializer.Meta.model.objects.filter(
                date=date,
                auditorium=auditorium,
                start_time__lte=end_time,
                end_time__gte=start_time,
            )
            if existing_bookings.exists():
                raise serializers.ValidationError(
                    f'Аудитория {Auditorium.objects.filter(id=auditorium).first()} занята на выбранное время и дату. Выберите другое время.')

            if self.request.user.is_superuser or (
                    self.request.user.has_perm(self.add_perm)
                    and self.request.user.has_perm(self.change_perm)
                    and self.request.user.is_staff
            ):
                serializer.save(
                    organazer=self.request.user,
                    auditorium=auditorium,
                    status='APPROVED',
                    who_approved=self.request.user,
                    datetime_approved=timezone.now()
                )
            else:
                serializer.save(
                    organazer=self.request.user,
                    auditorium=auditorium,
                )