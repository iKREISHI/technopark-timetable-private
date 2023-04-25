from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from users.models.university import University_Unit


class UniversityUnitCreateForm(forms.ModelForm):

    class Meta:
        model = University_Unit
        fields = ('name', 'abbreviation', 'info')