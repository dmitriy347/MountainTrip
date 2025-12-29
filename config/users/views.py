from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class UserLoginView(LoginView):
    """Класс-представление для авторизации пользователя."""
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }

    def form_valid(self, form):
        """Вывод сообщения об успешной авторизации."""
        messages.success(self.request, 'Вы успешно вошли в систему')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Класс-представление для выхода пользователя из системы."""
    def dispatch(self, request, *args, **kwargs):
        """Вывод сообщения об успешном выходе из системы."""
        messages.success(request, 'Вы вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    """Класс-представление для регистрации нового пользователя."""
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': 'Регистрация'
    }
