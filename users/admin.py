from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.models.university import University_Unit, University_Building, Auditorium_Type, Auditorium

# Register your models here.
User = get_user_model()


# @admin.register(User)
# class UserAdmin(UserAdmin):
#     pass


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'patronymic', 'university_unit', 'phone_number', 'is_verificated', 'info')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic', 'university_unit', 'phone_number', 'is_verificated', 'info')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(University_Unit)
admin.site.register(University_Building)
admin.site.register(Auditorium_Type)
admin.site.register(Auditorium)
