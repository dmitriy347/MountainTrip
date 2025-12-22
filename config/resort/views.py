from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string

from .forms import TripForm
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


def trip_create(request):
    """Создание новой поездки"""
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()

    data = {
        'title': 'Новая поездка',
        'form': form,
    }
    return render(request, 'resort/trip_form.html', context=data)


def trip_edit(request, trip_id):
    return HttpResponse(f"Редактирование поездки")







def about(request):
    return render(request, 'resort/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Вход на сайт")


def page_not_found(request, exception):
    """Обработчик ошибки 404"""
    return HttpResponseNotFound("404 страница не найдена", status=404)



