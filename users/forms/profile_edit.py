from django import forms
from users.models.users import User
from phonenumber_field.formfields import PhoneNumberField


class UserProfileEditForm(forms.ModelForm):
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        }),
    )

    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
    )

    patronymic = forms.CharField(
        label="Отчество",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше отчество'
        }),
    )

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        }),
    )

    phone_number = PhoneNumberField(
        label='Мобильный телефон', region='RU',
    )

    class Meta:
        model = User
        fields = (
            'last_name', 'first_name', 'patronymic', 'email', 'phone_number'
        )