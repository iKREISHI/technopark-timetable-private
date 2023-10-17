from django.urls import include, path
from api_v0.views.timetable_item_baseinfo import (
    TimetableItemDetailView
)
from api_v0.views.BookingWeek import (
    BookingCurrentWeekAPIView,
    BookingWeekAPIView, BookingByWeekAPIView,
    BookingWeekMinimalAPIView
)
from api_v0.views.BookingCreate import BookingCreateAPIView, ReservationCreateAPIView
from api_v0.views.AuditoriumView import getAuditoriumAPIView


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
        'booking-week/<str:monday>-<str:sunday>/', BookingWeekAPIView.as_view(),
        name='booking-week',
    ),
    path(
        'booking-create/', BookingCreateAPIView.as_view(),
        name='booking-create'
    ),
    path(
        'add-reservation/', ReservationCreateAPIView.as_view(),
        name='add-reservation-api'
    ),
    path(
        'get-auditoriums/', getAuditoriumAPIView.as_view(),
        name='get-auditoriums',
    ),
    path(
        'get-booking-week/<str:monday>-<str:sunday>/', BookingWeekMinimalAPIView.as_view(),
        name='get-booking-week',
    ),
    # path(
    #     'booking-by-week/<str:monday>-<str:sunday>/', BookingByWeekAPIView.as_view(),
    #     name='booking-by-week',
    # ),
]