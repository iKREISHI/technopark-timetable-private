from rest_framework import serializers
from users.models.users import (
    User
)


class UserBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'patronymic'
        ]


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id'
        ]