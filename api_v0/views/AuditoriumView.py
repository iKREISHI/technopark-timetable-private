from datetime import date, timedelta
from rest_framework import generics
from api_v0.serializers.University import AuditoriumSerializer, AuditoriumsSerializer, UniversityUnitSerializer
from users.models.university import Auditorium, Auditorium_Type, University_Unit
from django.db.models import Value, CharField
from django.db.models.functions import Cast


class getAuditoriumAPIView(generics.ListAPIView):
    serializer_class = AuditoriumSerializer

    def get_queryset(self):
        queryset = (Auditorium.objects.filter(university_unit__show_in_timetable=True)
                    .order_by(Cast('name', CharField()), 'name'))
        return queryset


class getAuditoriumByUUAPIView(generics.ListAPIView):
    serializer_class = AuditoriumSerializer

    def get_queryset(self):
        id_university_unit = self.kwargs['id_university_unit']
        # queryset = Auditorium.objects.filter(
        #     university_unit__show_in_timetable=True,
        #     university_unit=University_Unit.objects.get(id=id_university_unit),
        # ).all()
        queryset = Auditorium.objects.filter(
            university_unit__show_in_timetable=True,
            university_unit=University_Unit.objects.get(id=id_university_unit),
        ).order_by(Cast('name', CharField()), 'name')
        return queryset


class getAuditoriumsListAPIView(generics.ListAPIView):
    serializer_class = AuditoriumsSerializer

    def get_queryset(self):
        queryset = Auditorium.objects.filter(university_unit__show_in_timetable=True).order_by('name', 'id').all()
        return queryset


class getAuditoriumByUUListAPIView(generics.ListAPIView):
    serializer_class = AuditoriumsSerializer

    def get_queryset(self):
        id_university_unit = self.kwargs['id_university_unit']
        queryset = Auditorium.objects.filter(
            university_unit__show_in_timetable=True,
            university_unit=University_Unit.objects.get(id=id_university_unit),
        )
        return queryset


class getUniversityUnitListAPIView(generics.ListAPIView):
    serializer_class = UniversityUnitSerializer

    def get_queryset(self):
        queryset = University_Unit.objects.filter(
            show_in_timetable=True,
        ).all()
        return queryset
