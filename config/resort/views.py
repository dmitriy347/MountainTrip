from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},]

resort = [
    {'name': 'Губаха', 'region': 'Пермский край', 'id': 1},
    {'name': 'Шерешеш', 'region': 'Кемеровская область', 'id': 2},
    {'name': 'Белая', 'region': 'Свердловская область', 'id': 3},
]

def home(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'resorts': resort,
    }
    return render(request, 'resort/home.html', context=data)


def resort_detail(request, resort_id):
    return render(request, 'resort/resort_detail.html')


def resort_list(request):
    context = {
        'resorts': resort,
    }
    return render(request, 'resort/resort_list.html', context=context)


def trip_detail(request, trip_id):
    return render(request, 'resort/trip_detail.html')


def trip_list(request):
    trips = [
        {
            'id': 1,
            'resort': 'Губаха',
            'start_date': '2024-02-10',
            'end_date': '2024-02-15',
        }
    ]
    return render(request, 'resort/trip_list.html', {'trips': trips})

def trip_create(request):
    return HttpResponse("Создание новой поездки")


def trip_edit(request, trip_id):
    return HttpResponse(f"Редактирование поездки")




def about(request):
    return render(request, 'resort/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request, post_id):
    return render(request, 'resort/post.html')


def add_page(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Вход на сайт")


def page_not_found(request, exception):
    """Обработчик ошибки 404"""
    return HttpResponseNotFound("404 страница не найдена", status=404)



