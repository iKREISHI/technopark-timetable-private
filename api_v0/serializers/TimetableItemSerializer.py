from rest_framework import serializers
from timetable.models.timetable import (
    TimetableItem,
    Type_TimetableItem
)
from users.models.university import (
    Auditorium
)
from api_v0.serializers.Users import (
    UserBaseInfoSerializer,
    UserMinimalSerializer,
)
from api_v0.serializers.University import AuditoriumSerializer, AuditoriumMinimalSerializer


class TypeTimetableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_TimetableItem
        fields = '__all__'


class TypeTimetableMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_TimetableItem
        fields = [
            'id', 'name'
        ]


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


class BookingSerialazer(serializers.ModelSerializer):
    organazer = UserMinimalSerializer()
    type = TypeTimetableMinimalSerializer()
    auditorium = AuditoriumMinimalSerializer(many=True)
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
        fields = '__all__'


class TimetableReservationSerializer(serializers.ModelSerializer):
    auditorium = AuditoriumSerializer(many=True)
    date = serializers.DateField(format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    class Meta:
        model = TimetableItem
        fields = '__all__'


class TimetableAuditoriumReservationSerializer(serializers.ModelSerializer):
    timetable = TimetableItemSerializer(many=True)

    class Meta:
        model = Auditorium,
        fields = '__all__'
