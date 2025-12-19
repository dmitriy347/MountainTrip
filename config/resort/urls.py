from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resort_detail/<int:resort_id>', views.resort_detail, name='resort_detail'),
    path('resort_list/', views.resort_list, name='resort_list'),
    path('trip_detail/<int:trip_id>', views.trip_detail, name='trip_detail'),
    path('trip_list/', views.trip_list, name='trip_list'),
    path('trip_create/', views.trip_create, name='trip_create'),
    path('trip_edit/<int:trip_id>', views.trip_edit, name='trip_edit'),
    path('login/', views.login, name='login'),

    path('about/', views.about, name='about'),
    path('addpage/', views.add_page, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:post_id>/', views.show_post, name='post'),

]
