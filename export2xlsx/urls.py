from django.urls import include, path
from export2xlsx.views.test import my_view
from export2xlsx.views.views import ExcelDownloadWeekView

urlpatterns = [
    # path(
    #   'test123/', my_view, name='test123'
    # ),
    path(
        'get-file-schedule/<str:monday>-<str:sunday>/<int:university_id>/',
        ExcelDownloadWeekView.as_view(),
        name='get-file-schedule'
    ),
]