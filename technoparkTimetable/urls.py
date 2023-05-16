from django.contrib import admin
from django.urls import path, include
from users.views.homepage import home
# from timetable.views import
from timetable.views.timetable_current_week import TimeTableCurrentWeekView

urlpatterns = [
    path('admin/', admin.site.urls, name='main-admin'),
    path('', TimeTableCurrentWeekView.as_view(), name='homepage'),
    path('users/', include('users.urls')),
    path('timetable/', include('timetable.urls')),
    path('captcha/', include('captcha.urls')),

]