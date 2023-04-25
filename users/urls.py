from django.urls import include, path
from users.views.registration import Register
from users.views.university import AddUniversityUnit, ViewUniversityUnit

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('add-univerisy-unit/', AddUniversityUnit.as_view(), name='add-university-unit'),
    path('view-university-unit/', ViewUniversityUnit.as_view(), name='view-university-unit'),



]