from django.contrib import admin
from django.urls import path, include
from users.views.homepage import home

urlpatterns = [
    path('admin/', admin.site.urls, name='main-admin'),
    path('', home, name='homepage'),
    path('users/', include('users.urls')),
]