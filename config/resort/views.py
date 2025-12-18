from django.http import HttpResponse


def home(request):
    return HttpResponse("Это страница home")

