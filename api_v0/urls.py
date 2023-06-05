from django.urls import include, path
from api_v0.views.timetable_item_baseinfo import (
    TimetableItemDetailView
)
from api_v0.views.BookingWeek import BookingCurrentWeekAPIView
from api_v0.views.BookingCreate import BookingCreateAPIView


urlpatterns = [
    path(
        'timetable-item-info/<int:id>/', TimetableItemDetailView.as_view(),
        name='timetable-item-info'
    ),
    path(
        'booking-current-week/<int:auditorium_id>/', BookingCurrentWeekAPIView.as_view(),
        name='booking-current-week'
    ),
    path(
        'booking-create/', BookingCreateAPIView.as_view(),
        name='booking-create'
    ),
]