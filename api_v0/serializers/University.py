from rest_framework import serializers
from users.models.university import (
    Auditorium, University_Unit
)


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = '__all__'


class AuditoriumMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auditorium
        fields = [
            'id', 'name'
        ]


class UniversityUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = University_Unit
        fields = [
            'id', 'name', 'abbreviation',
            'show_in_timetable', 'default_show'
        ]


class AuditoriumsSerializer(serializers.ModelSerializer):
    university_unit = UniversityUnitSerializer()

    class Meta:
        model = Auditorium
        fields = [
            'id', 'name', 'university_unit',
            'area', 'capacity',
        ]