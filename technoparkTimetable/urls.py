from django.contrib import admin
from django.urls import path, include
from users.views.homepage import home
# from timetable.views import
from timetable.views.timetable_current_week import TimeTableCurrentWeekView
from timetable.views.timtable import CurrentScheduleView

urlpatterns = [
    path('admin/', admin.site.urls, name='main-admin'),
    # path('', TimeTableCurrentWeekView.as_view(), name='homepage'),
    path('', CurrentScheduleView.as_view(), name='homepage'),
    path('users/', include('users.urls')),
    path('timetable/', include('timetable.urls')),
    path('captcha/', include('captcha.urls')),
    path('api/v0/', include('api_v0.urls'))

]