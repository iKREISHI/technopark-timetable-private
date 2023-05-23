from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField, CaptchaTextInput
from users.models.university import University_Unit
from users.models.users import User as UserModel
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


User = get_user_model()


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(
        label="Имя пользователя*",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя пользователя'
        }),
        required=True
    )

    last_name = forms.CharField(
        label="Фамилия*",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        }),
        required=True
    )

    first_name = forms.CharField(
        label="Имя*",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
        required=True
    )

    patronymic = forms.CharField(
        label="Отчество",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше отчество'
        }),
        required=False
    )

    email = forms.EmailField(
        label=_("Email*"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        }),
        required=True
    )

    '''phone_number = forms.CharField(
        label="Номер мобильного телефона*",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш номер мобильного телефона'
        }),
        required=True
    )'''

    phone_number = PhoneNumberField(
       label='Мобильный телефон', region='RU',

    )

    university_unit = forms.ModelChoiceField(
        queryset=University_Unit.objects.all(),
        label="Университетское подразделение*",
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        required=True
    )

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Пароль*"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'placeholder': 'Введите ваш пароль'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля*"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'placeholder': 'Подтвердите ваш пароль'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    captcha = CaptchaField(
        label="Подтвердите проверку*",
        widget=CaptchaTextInput(attrs={
            'placeholder': 'введите текст с картинки',
        }),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username", "last_name", "first_name", "patronymic", "email",
            "phone_number", "university_unit", "password1", "password2", "captcha"
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email'),
        phone_number = cleaned_data.get('phone_number')

        if username and email and phone_number:
            user = UserModel.objects.filter(username=username, email=email, phone_number=phone_number)
            if user.exists():
                self.add_error(None, f'Пользователь с  именем {username} существует')