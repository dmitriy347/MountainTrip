from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TripForm, TripMediaForm
from .mixins import OwnerQuerySetMixin
from .models import Resort, Trip, TripMedia



def index(request):
    """Главная страница"""
    data = {
        'title': 'Горнолыжные курорты России',
    }
    return render(request, 'resort/index.html', context=data)


class ResortDetailView(DetailView):
    """
    Класс-представление для страницы курорта
    После выбора курорта происходит перенаправление по get_absolute_url модели Resort
    """
    model = Resort
    template_name = 'resort/resort_detail.html'
    context_object_name = 'resort'
    slug_field = 'slug'
    slug_url_kwarg = 'resort_slug'

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст заголовок страницы и фильтрацию поездки по текущему пользователю и публичности
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        user = self.request.user                # Получаем текущего пользователя
        trips_qs = self.object.trips.all()      # Все поездки, связанные с курортом

        counts = trips_qs.aggregate(    # словарь counts с общим количеством поездок и количеством публичных поездок
            total=Count('id'),
            public=Count('id', filter=Q(is_public=True)))

        # 0. Количество поездок к курорту (видят все)
        context['total_trips_count'] = counts.get('total', 0)
        context['public_trips_count'] = counts.get('public', 0)

        # 1. Гость - не видит список поездок
        if not user.is_authenticated:
            context['trips'] = None
            return context

        # 2. Авторизованные
        context['trips'] = trips_qs.filter(
            Q(is_public=True) | Q(user=user)
        ).select_related('user', 'resort')                # Оптимизация: сразу подтягиваем связанные объекты User
        return context


class ResortListView(ListView):
    """Класс-представление для списка курортов"""
    model = Resort
    template_name = 'resort/resort_list.html'
    context_object_name = 'resorts'
    paginate_by = 5


class TripDetailView(LoginRequiredMixin, DetailView):
    """Класс-представление для страницы поездки"""
    model = Trip
    template_name = 'resort/trip_detail.html'
    context_object_name = 'trip'
    pk_url_kwarg = 'trip_id'

    def get_context_data(self, **kwargs):
        """Добавляем в контекст заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = f"Поездка в {self.object.resort.name}"
        context['media_list'] = self.object.media.all()
        return context

    def get_queryset(self):
        """Фильтрация поездок по текущему пользователю и публичности"""
        user = self.request.user
        return Trip.objects.filter(
            Q(is_public=True) | Q(user=user)
        )


class TripListView(LoginRequiredMixin, ListView):
    """Класс-представление для списка поездок пользователя"""
    model = Trip
    template_name = 'resort/trip_list.html'
    context_object_name = 'trips'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """Добавляем в контекст заголовок страницы"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои поездки'
        return context

    def get_queryset(self):
        """Фильтрация поездок по текущему пользователю"""
        return (
            Trip.objects
                .select_related('resort')       # Оптимизация: сразу подтягиваем связанные объекты Resort
                .filter(user=self.request.user)
        )


class TripCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-представление для создания новой поездки
    После сохранения происходит перенаправление по get_absolute_url модели Trip
    """
    form_class = TripForm
    template_name = 'resort/trip_form.html'
    extra_context = {
        'title': 'Новая поездка',
    }

    def form_valid(self, form):
        """
        Дополняем форму данными о текущем пользователе перед сохранением.
        Добавляем сообщение об успешном создании.
        """
        form.instance.user = self.request.user  # Альтернативный способ присвоения пользователя через form.instance (это объект модели Trip, который будет сохранен)
        messages.success(self.request, "Поездка успешно создана.")
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, OwnerQuerySetMixin, UpdateView):
    """
    Класс-представление для редактирования поездки
    После сохранения происходит перенаправление по get_absolute_url модели Trip
    Доступ к редактированию ограничен владельцем поездки через миксин OwnerQuerySetMixin
    """
    form_class = TripForm
    model = Trip
    template_name = 'resort/trip_form.html'
    pk_url_kwarg = 'trip_id'
    owner_field = 'user'
    extra_context = {
        'title': 'Редактирование поездки',
    }

    def form_valid(self, form):
        """Добавляем сообщение об успешном сохранении"""
        messages.success(self.request, "Поездка успешно изменена.")
        return super().form_valid(form)


class TripDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, DeleteView):
    """
    Класс-представление для удаления поездки
    После удаления происходит перенаправление на страницу списка поездок
    Доступ к удалению ограничен владельцем поездки через миксин OwnerQuerySetMixin
    """
    model = Trip
    template_name = 'resort/trip_confirm_delete.html'
    context_object_name = 'trip'
    pk_url_kwarg = 'trip_id'
    success_url = reverse_lazy('trip_list')
    owner_field = 'user'
    extra_context = {
        'title': 'Удаление поездки',
    }

    def form_valid(self, form):
        """Добавляем сообщение об успешном удалении"""
        messages.success(self.request, "Поездка удалена.")
        return super().form_valid(form)


class TripMediaAddView(LoginRequiredMixin, CreateView):
    """
    Класс-представление для добавления медиафайлов к поездке
    После сохранения происходит перенаправление по get_absolute_url модели TripMedia
    """
    form_class = TripMediaForm
    template_name = 'resort/trip_media_form.html'
    extra_context = {
        'title': 'Добавить фото к поездке',
    }

    def form_valid(self, form):
        """Дополняем форму данными о текущей поездке перед сохранением"""
        trip_id = self.kwargs['trip_id']
        user = self.request.user    # Защита от добавления фото к чужой поездке
        trip = get_object_or_404(Trip, pk=trip_id, user=user)

        form.instance.trip = trip   # Привязываем медиафайл к поездке ДО сохранения
        messages.success(self.request, "Фото успешно добавлено.")
        return super().form_valid(form)


class TripMediaDeleteView(LoginRequiredMixin, OwnerQuerySetMixin, DeleteView):
    """
    Класс-представление для удаления медиафайлов из поездки
    Удаление медиафайла из файловой системы происходит автоматически с помощью сигнала post_delete
    Доступ к удалению ограничен владельцем медиафайлов через миксин OwnerQuerySetMixin
    """
    model = TripMedia
    template_name = 'resort/trip_media_confirm_delete.html'
    context_object_name = 'media'
    pk_url_kwarg = 'media_id'
    owner_field = 'trip__user'
    extra_context = {
        'title': 'Удаление фото из поездки',
    }

    def form_valid(self, form):
        """Добавляем сообщение об успешном удалении"""
        messages.success(self.request, "Фото удалено.")
        return super().form_valid(form)

    def get_success_url(self):
        """После удаления перенаправляем на страницу детали поездки"""
        return reverse_lazy('trip_detail', kwargs={'trip_id': self.object.trip.id})


def page_not_found(request, exception):
    """Обработчик ошибки 404"""
    return HttpResponseNotFound("404 страница не найдена", status=404)



