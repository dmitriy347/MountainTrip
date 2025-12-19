from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},]

data_db = [
    {'title': 'Первый курорт', 'content': 'Описание первого курорта', 'id': 1},
    {'title': 'Второй курорт', 'content': 'Описание второго курорта', 'id': 2},
    {'title': 'Третий курорт', 'content': 'Описание третьего курорта', 'id': 3},
]

def home(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'data_db': data_db,
    }
    return render(request, 'resort/home.html', context=data)


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



