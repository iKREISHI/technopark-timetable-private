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


class AuditoriumAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'type', 'building', 'area', 'capacity'
    )
    search_fields = (
        'name',
    )


class UniversityUnitAdminPanel(admin.ModelAdmin):
    list_display = (
        'name', 'abbreviation', 'info',
    )
    search_fields = (
        'name', 'abbreviation',
    )


class UniversityBuildingAdminPanel(admin.ModelAdmin):
    list_display = (
        'name', 'address', 'info'
    )
    search_fields = (
        'name', 'address',
    )


class AuditoriumTypeAdminPanel(admin.ModelAdmin):
    list_display = (
        'name', 'info',
    )
    search_fields = (
        'name',
    )


University_Unit._meta.verbose_name = 'Подразделение универститета'
University_Unit._meta.verbose_name_plural = 'Подразделения университета'

University_Building._meta.verbose_name = 'Корпус Университета'
University_Building._meta.verbose_name_plural = 'Корпуса Университета'

Auditorium_Type._meta.verbose_name = 'Тип аудитории'
Auditorium_Type._meta.verbose_name_plural = 'Типы аудиторий'

Auditorium._meta.verbose_name = 'Аудитория'
Auditorium._meta.verbose_name_plural = 'Аудитории'

admin.site.register(User, CustomUserAdmin)
admin.site.register(University_Unit, UniversityUnitAdminPanel)
admin.site.register(University_Building, UniversityBuildingAdminPanel)
admin.site.register(Auditorium_Type, AuditoriumTypeAdminPanel)
admin.site.register(Auditorium, AuditoriumAdmin)
