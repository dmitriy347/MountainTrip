from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания нового пользователя с дополнительными полями."""

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите свой email"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя пользователя",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с применением Bootstrap классов и русификацией лейблов."""
        super().__init__(*args, **kwargs)
        # Применяем Bootstrap классы к полям паролей
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )

        # Убираем стандартные подсказки Django
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    def clean_email(self):
        """Проверка уникальности email."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Имя пользователя",
            }
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
            }
        ),
    )
