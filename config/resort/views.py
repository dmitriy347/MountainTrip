from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TripForm, TripMediaForm
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
        """Добавляем в контекст заголовок и список поездок"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['trips'] = self.object.trips.all()
        return context


class ResortListView(ListView):
    """Класс-представление для списка курортов"""
    model = Resort
    template_name = 'resort/resort_list.html'
    context_object_name = 'resorts'


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
        """Фильтрация поездок по текущему пользователю"""
        return (
            Trip.objects
                .select_related('resort')   # Оптимизация: сразу подтягиваем связанные объекты Resort
                .prefetch_related('media')  # Оптимизация: сразу подтягиваем связанные объекты TripMedia
                .filter(user=self.request.user)
        )


class TripListView(LoginRequiredMixin, ListView):
    """Класс-представление для списка поездок пользователя"""
    model = Trip
    template_name = 'resort/trip_list.html'
    context_object_name = 'trips'

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
        """Дополняем форму данными о текущем пользователе перед сохранением"""
        form.instance.user = self.request.user  # Альтернативный способ присвоения пользователя через form.instance (это объект модели Trip, который будет сохранен)
        return super().form_valid(form)


class TripUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-представление для редактирования поездки
    После сохранения происходит перенаправление по get_absolute_url модели Trip
    """
    form_class = TripForm
    template_name = 'resort/trip_form.html'
    pk_url_kwarg = 'trip_id'
    extra_context = {
        'title': 'Редактирование поездки',
    }

    def get_queryset(self):
        """Фильтрация поездок по текущему пользователю для защиты от редактирования чужих поездок"""
        return Trip.objects.filter(user=self.request.user)


class TripDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления поездки
    После удаления происходит перенаправление на страницу списка поездок
    """
    model = Trip
    template_name = 'resort/trip_confirm_delete.html'
    context_object_name = 'trip'
    pk_url_kwarg = 'trip_id'
    success_url = reverse_lazy('trip_list')
    extra_context = {
        'title': 'Удаление поездки',
    }

    def get_queryset(self):
        """Фильтрация поездок по текущему пользователю для защиты от удаления чужих поездок"""
        return Trip.objects.filter(user=self.request.user)


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
        return super().form_valid(form)


class TripMediaDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления медиафайлов из поездки
    Удаление медиафайла из файловой системы происходит автоматически с помощью сигнала post_delete
    """
    model = TripMedia
    template_name = 'resort/trip_media_confirm_delete.html'
    context_object_name = 'media'
    pk_url_kwarg = 'media_id'
    extra_context = {
        'title': 'Удаление фото из поездки',
    }

    def get_queryset(self):
        """Фильтрация медиафайлов по текущему пользователю для защиты от удаления чужих медиафайлов"""
        return TripMedia.objects.filter(trip__user=self.request.user)

    def get_success_url(self):
        """После удаления перенаправляем на страницу детали поездки"""
        return reverse_lazy('trip_detail', kwargs={'trip_id': self.object.trip.id})


def login(request):
    return HttpResponse("Вход на сайт")


def page_not_found(request, exception):
    """Обработчик ошибки 404"""
    return HttpResponseNotFound("404 страница не найдена", status=404)



