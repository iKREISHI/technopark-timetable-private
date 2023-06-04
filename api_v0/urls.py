from django.urls import include, path
from api_v0.views.timetable_item_baseinfo import (
    TimetableItemDetailView
)
urlpatterns = [
    path('timetable-item-info/<int:id>/', TimetableItemDetailView.as_view(), name='timetable-item-info'),

]