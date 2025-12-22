from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('resort/<int:resort_id>', views.resort_detail, name='resort_detail'),
    path('resorts/', views.resort_list, name='resort_list'),
    path('trip/<int:trip_id>', views.trip_detail, name='trip_detail'),
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create', views.trip_create, name='trip_create'),
    path('trips/<int:trip_id>/edit', views.trip_edit, name='trip_edit'),
    path('login/', views.login, name='login'),



    path('about/', views.about, name='about'),
    path('addpage/', views.add_page, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:post_id>/', views.show_post, name='post'),

]
