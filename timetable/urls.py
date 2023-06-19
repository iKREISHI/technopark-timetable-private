from django.urls import include, path
from timetable.views.reservation import AddTimeTableReservation
from timetable.views.user_reservations import UserReservationsList, UserReservationUpdateView
from timetable.views.admin_reservations import AdminApproveReservationList, AdminApproveReservation
from timetable.views.timetable_current_week import (
    TimeTableCurrentWeekView,
)
from timetable.views.timetable_item_edit import TimeTableItemUpdateView
from timetable.views.timetable_item_delete import TimetableItemDeleteView
from timetable.views.timetable_week import TimetableWeekView

from timetable.views.booking.booking import (
    BookingTimeTableView,
    BookingTimeTableWeekView
)
from timetable.views.list_week import ListWeekView
from timetable.views.list_auditorium import ListAuditoriumView
from timetable.views.timtable import ScheduleView

urlpatterns = [
    path('add-reservation/', AddTimeTableReservation.as_view(), name='add-user-reservation'),
    path('list-reservation/', UserReservationsList.as_view(), name='list-user-reservation'),
    path(
        'reservation/<int:pk>/update', UserReservationUpdateView.as_view(),
        name='update-user-reservation'
    ),
    path('list-admin-reservation/', AdminApproveReservationList.as_view(), name='list-admin-reservation'),
    path(
        'approve-reservation/<int:reservation_id>/<str:status>/',
        AdminApproveReservation.as_view(), name='approve-reservation'
    ),
    path('current-week/', TimeTableCurrentWeekView.as_view(), name='current-week'),
    # path('current-week-json/', TimeTableCurrentWeekJSONView.as_view(), name='current-week-json'),
    path('item/<int:pk>/update/', TimeTableItemUpdateView.as_view(), name='timetableitem-update'),
    path('item/<int:pk>/delete', TimetableItemDeleteView.as_view(), name='timetableitem-delete'),
    path('week/<str:monday>-<str:sunday>', TimetableWeekView.as_view(), name='timetable-week'),
    path('booking-timetable/<int:auditorium_id>', BookingTimeTableView.as_view(), name='booking-timetable'),
    path(
        'booking-timetable/<int:auditorium_id>/<str:monday>-<str:sunday>',
        BookingTimeTableWeekView.as_view(),
        name='booking-timetable-week'
    ),
    path('list-week', ListWeekView.as_view(), name='list-week'),
    path('list-auditoriums/<str:monday>-<str:sunday>', ListAuditoriumView.as_view(), name='list-auditoriums'),
    path('schedule/<str:monday>-<str:sunday>', ScheduleView.as_view(), name='schedule'),
]