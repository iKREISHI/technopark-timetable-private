from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.models.university import University_Unit, University_Building, Auditorium_Type, Auditorium

# Register your models here.
User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


admin.site.register(University_Unit)
admin.site.register(University_Building)
admin.site.register(Auditorium_Type)
admin.site.register(Auditorium)
