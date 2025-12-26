from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserLoginView(LoginView):
    """Класс-представление для авторизации пользователя."""
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """"""
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(CreateView):
    """"""
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    extra_context = {
        'title': 'Регистрация'
    }

    def form_valid(self, form):
        """"""
        messages.success(self.request, 'Регистрация прошла успешно')
        return super().form_valid(form)