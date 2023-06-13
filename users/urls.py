from django.urls import include, path
from django.contrib.auth import views
from users.views.registration import Register
from users.views.University.university_unit import AddUniversityUnit, ViewUniversityUnit
from users.views.University.building import AddUniversityBuilding, ViewUniversityBuilding
from users.views.University.auditorium import AddAuditorium, AddAuditoriumType, ViewAuditorium, ViewAuditoriumType
from users.views.user_confirmation import UserConfirmation, ConfirmNewUser
from users.views.waiting_user_confirmation import WaitingUserConfirm
from users.views.profile import ProfileView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name='user/change_password.html',
            success_url='/users/password_changed/'
        ),
        name="password_change"
    ),
    path(
        "password_changed/",
        views.PasswordChangeDoneView.as_view(
            template_name='user/password_changed.html',
        ),
        name="password_changed",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path('register/', Register.as_view(), name='register'),
    path('add-univerisy-unit/', AddUniversityUnit.as_view(), name='add-university-unit'),
    path('view-university-unit/', ViewUniversityUnit.as_view(), name='view-university-unit'),
    path('add-univerisy-building/', AddUniversityBuilding.as_view(), name='add-university-building'),
    path('view-university-building/', ViewUniversityBuilding.as_view(), name='view-university-building'),
    path('add-university-auditorium/', AddAuditorium.as_view(), name='add-university-auditorium'),
    path('view-university-auditorium/', ViewAuditorium.as_view(), name='view-university-auditorium'),
    path('add-university-auditorium-type/', AddAuditoriumType.as_view(), name='add-university-auditorium-type'),
    path('view-university-auditorium-type/', ViewAuditoriumType.as_view(), name='view-university-auditorium-type'),
    path('list-admin-confirm-user/', UserConfirmation.as_view(), name='list-admin-confirm-user'),
    path('confirm-new-user/<int:user_id>/<str:str>', ConfirmNewUser.as_view(), name='confirm-new-user'),
    path('waiting-user-confirm/', WaitingUserConfirm.as_view(), name='waiting-user-confirm'),
    path('profile', ProfileView.as_view(), name="user-profile"),
]