from django.urls import include, path
from api_v0.views.timetable_item_baseinfo import (
    TimetableItemDetailView
)
from api_v0.views.BookingWeek import (
    BookingCurrentWeekAPIView,
    BookingWeekAPIView,
    BookingWeekMinimalAPIView,
    BookingCurrentWeekMinimalAPIView,
    BookingByUUListAPIView,
    BookingByUUCurrentWeekListAPIView,
)
from api_v0.views.BookingCreate import BookingCreateAPIView, ReservationCreateAPIView
from api_v0.views.AuditoriumView import (
    getAuditoriumAPIView,
    getAuditoriumsListAPIView,
    getAuditoriumByUUListAPIView, getAuditoriumByUUAPIView,
    getUniversityUnitListAPIView
)


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
        'get-auditoriums/<int:id_university_unit>/', getAuditoriumByUUAPIView.as_view(),
        name='get-auditoriums-by-uu',
    ),
    path(
        'get-booking-week/<str:monday>-<str:sunday>/', BookingWeekMinimalAPIView.as_view(),
        name='get-booking-week',
    ),
    path(
        'get-list-auditoriums/', getAuditoriumsListAPIView.as_view(),
        name='get-list-auditoriums',
    ),
    path(
        'get-list-auditoriums/<int:id_university_unit>/', getAuditoriumByUUListAPIView.as_view(),
        name='get-list-auditoriums',
    ),
    path(
        'get-booking-current-week/', BookingCurrentWeekMinimalAPIView.as_view(),
        name='get-booking-current-week',
    ),
    path(
        'get-booking-week/<int:id_university_unit>/<str:monday>-<str:sunday>/',
        BookingByUUListAPIView.as_view(),
        name='get-booking-week-by-uu',
    ),
    path(
        'get-booking-current-week/<int:id_university_unit>/',
        BookingByUUCurrentWeekListAPIView.as_view(),
        name='get-booking-current-week-by-uu',
    ),
    path(
        'get-university-unit/', getUniversityUnitListAPIView.as_view(),
        name='get-university-unit'
    ),
]