from rest_framework import serializers
from users.models.university import (
    Auditorium
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