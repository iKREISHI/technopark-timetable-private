from datetime import date, timedelta
from rest_framework import generics
from api_v0.serializers.University import AuditoriumSerializer, AuditoriumsSerializer
from users.models.university import Auditorium, Auditorium_Type


class getAuditoriumAPIView(generics.ListAPIView):
    serializer_class = AuditoriumSerializer

    def get_queryset(self):
        queryset = Auditorium.objects.filter(university_unit__show_in_timetable=True).all()
        return queryset


class getAuditoriumsListAPIView(generics.ListAPIView):
    serializer_class = AuditoriumsSerializer

    def get_queryset(self):
        queryset = Auditorium.objects.filter(university_unit__show_in_timetable=True).order_by('name', 'id').all()
        return queryset
