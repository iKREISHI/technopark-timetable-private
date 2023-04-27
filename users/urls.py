from django.urls import include, path
from users.views.registration import Register
from users.views.University.university_unit import AddUniversityUnit, ViewUniversityUnit
from users.views.University.building import AddUniversityBuilding, ViewUniversityBuilding
from users.views.University.auditorium import AddAuditorium, AddAuditoriumType, ViewAuditorium, ViewAuditoriumType

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('add-univerisy-unit/', AddUniversityUnit.as_view(), name='add-university-unit'),
    path('view-university-unit/', ViewUniversityUnit.as_view(), name='view-university-unit'),
    path('add-univerisy-building/', AddUniversityBuilding.as_view(), name='add-university-building'),
    path('view-university-building/', ViewUniversityBuilding.as_view(), name='view-university-building'),
    path('add-university-auditorium/', AddAuditorium.as_view(), name='add-university-auditorium'),
    path('view-university-auditorium/', ViewAuditorium.as_view(), name='view-university-auditorium'),
    path('add-university-auditorium-type/', AddAuditoriumType.as_view(), name='add-university-auditorium-type'),
    path('view-university-auditorium-type/', ViewAuditoriumType.as_view(), name='view-university-auditorium-type'),
]