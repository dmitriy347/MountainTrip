from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string

from .forms import TripForm, TripMediaForm
from .models import Resort, Trip




def index(request):
    """Главная страница"""
    resorts = Resort.objects.all()
    data = {
        'title': 'Горнолыжные курорты России',
        'resorts': resorts,
    }
    return render(request, 'resort/index.html', context=data)


def resort_detail(request, resort_id):
    """Страница курорта"""
    resort = get_object_or_404(Resort, pk=resort_id)
    trips = resort.trips.all()
    data = {
        'title': resort.name,
        'resort': resort,
        'trips': trips,
    }
    return render(request, 'resort/resort_detail.html', context=data)


def resort_list(request):
    """Список курортов"""
    resorts = Resort.objects.all()

    context = {
        'title': 'Список курортов',
        'resorts': resorts,
    }
    return render(request, 'resort/resort_list.html', context=context)


def trip_detail(request, trip_id):
    """Страница поездки"""
    trip = get_object_or_404(Trip, pk=trip_id)
    data = {
        'title': f"Поездка в {trip.resort.name}",
        'trip': trip,
    }
    return render(request, 'resort/trip_detail.html', context=data)


def trip_list(request):
    """Список поездок пользователя"""
    trips = Trip.objects.filter(user=request.user)
    data = {
        'title': 'Мои поездки',
        'trips': trips,
    }
    return render(request, 'resort/trip_list.html', context=data)


@login_required
def trip_create(request):
    """Создание новой поездки"""
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)  # Создаем объект, но не сохраняем в БД
            trip.user = request.user    # Дополняем форму данными о текущем пользователе
            trip.save()                 # Только теперь сохраняем объект в БД
            return redirect('trip_list')
    else:
        form = TripForm()

    data = {
        'title': 'Новая поездка',
        'form': form,
    }
    return render(request, 'resort/trip_form.html', context=data)


@login_required
def trip_edit(request, trip_id):
    """Редактирование поездки"""
    trip = get_object_or_404(Trip, pk=trip_id)

    # Защита от редактирования чужих поездок
    if trip.user != request.user:
        raise Http404("Поездка не найдена")

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)    # Заполняем форму данными из объекта trip
        if form.is_valid():
            form.save()
            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = TripForm(instance=trip)

    data = {
        'title': 'Редактирование поездки',
        'form': form,
    }
    return render(request, 'resort/trip_form.html', context=data)


@login_required
def trip_delete(request, trip_id):
    """Удаление поездки"""
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.user != request.user:
        raise Http404("Поездка не найдена")
    if request.method == 'POST':
        trip.delete()
        return redirect('trip_list')

    data = {
        'title': 'Удаление поездки',
        'trip': trip,
    }
    return render(request, 'resort/trip_confirm_delete.html', context=data)


@login_required
def trip_media_add(request, trip_id):
    """Добавления медиафайлов к поездке"""
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.user != request.user:
        raise Http404("Поездка не найдена")

    if request.method == 'POST':
        form = TripMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False) # Создаем объект, но не сохраняем в БД
            media.trip = trip               # Привязываем медиафайл к поездке
            media.save()                    # Сохраняем объект в БД
            return redirect('trip_detail', trip_id=trip.id)
    else:
        form = TripMediaForm()

    data = {
        'title': 'Добавить фото к поездке',
        'form': form,
        'trip': trip,
    }
    return render(request, 'resort/trip_media_form.html', context=data)






def about(request):
    return render(request, 'resort/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Вход на сайт")


def page_not_found(request, exception):
    """Обработчик ошибки 404"""
    return HttpResponseNotFound("404 страница не найдена", status=404)



