from datetime import date, timedelta
from rest_framework import generics
from api_v0.serializers.University import AuditoriumSerializer
from users.models.university import Auditorium, Auditorium_Type


class getAuditoriumAPIView(generics.ListAPIView):
    serializer_class = AuditoriumSerializer

    def get_queryset(self):
        queryset = Auditorium.objects.all()
        return queryset
