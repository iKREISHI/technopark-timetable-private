from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from users.models.university import University_Unit, University_Building, Auditorium_Type, Auditorium


class UniversityUnitCreateForm(forms.ModelForm):
    class Meta:
        model = University_Unit
        fields = ('name', 'abbreviation', 'info')


class BuildingCreateForm(forms.ModelForm):
    class Meta:
        model = University_Building
        fields = ('name', 'address', 'info')


class AuditoriumTypeCreateForm(forms.ModelForm):
    class Meta:
        model = Auditorium_Type
        fields = ('name', 'info')


class AuditoriumCreateForm(forms.ModelForm):
    class Meta:
        model = Auditorium
        fields = (
            'name', 'building', 'university_unit',
            'type', 'area', 'capacity', 'info'
        )