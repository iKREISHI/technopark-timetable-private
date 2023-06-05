from rest_framework import serializers
from timetable.models.timetable import (
    TimetableItem,
    Type_TimetableItem
)
from api_v0.serializers.Users import UserBaseInfoSerializer
from api_v0.serializers.University import AuditoriumSerializer


class TypeTimetableItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type_TimetableItem
        fields = '__all__'


class TimetableItemBaseInfoSerializer(serializers.ModelSerializer):
    organazer = UserBaseInfoSerializer()
    type = TypeTimetableItemSerializer()
    auditorium = AuditoriumSerializer(many=True)
    date = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    class Meta:
        model = TimetableItem
        fields = [
            'id', 'name', 'organazer', 'type', 'amount_people',
            'date', 'start_time', 'end_time', 'auditorium', 'info'
        ]


class TimetableItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    class Meta:
        model = TimetableItem
        fields = [
            'id', 'name', 'organazer', 'type', 'amount_people',
            'date', 'start_time', 'end_time', 'auditorium', 'info'
        ]
