from rest_framework import generics, permissions
from api_v0.serializers.TimetableItemSerializer import TimetableItemBaseInfoSerializer
from timetable.models.timetable import TimetableItem


class TimetableItemDetailView(generics.RetrieveAPIView):
    queryset = TimetableItem.objects.all()
    serializer_class = TimetableItemBaseInfoSerializer
    lookup_field = 'id'
    # permission_classes = [permissions.IsAuthenticated]