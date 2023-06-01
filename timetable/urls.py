from django.urls import include, path
from timetable.views.reservation import AddTimeTableReservation
from timetable.views.user_reservations import UserReservationsList, UserReservationUpdateView
from timetable.views.admin_reservations import AdminApproveReservationList, AdminApproveReservation
from timetable.views.timetable_current_week import (
    TimeTableCurrentWeekView,
)
from timetable.views.timetable_item_edit import TimeTableItemUpdateView
from timetable.views.timetable_item_delete import TimeTableItemDeleteView
from timetable.views.timetable_week import TimetableWeekView

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
    path('item/<int:pk>/delete', TimeTableItemDeleteView.as_view(), name='timetableitem-delete'),
    path('week-<str:monday>-<str:sunday>', TimetableWeekView.as_view(), name='timetable-week'),
]