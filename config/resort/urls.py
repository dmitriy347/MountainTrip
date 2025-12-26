from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('resort/<slug:resort_slug>', views.ResortDetailView.as_view(), name='resort_detail'),
    path('resorts/', views.ResortListView.as_view(), name='resort_list'),
    path('trip/<int:trip_id>', views.TripDetailView.as_view(), name='trip_detail'),
    path('trips/', views.TripListView.as_view(), name='trip_list'),
    path('trips/create', views.TripCreateView.as_view(), name='trip_create'),
    path('trips/<int:trip_id>/edit', views.TripUpdateView.as_view(), name='trip_edit'),
    path('trips/<int:trip_id>/delete', views.TripDeleteView.as_view(), name='trip_delete'),
    path('trips/<int:trip_id>/media/add', views.TripMediaAddView.as_view(), name='trip_media_add'),
    path('media/<int:media_id>/delete/', views.TripMediaDeleteView.as_view(), name='trip_media_delete'),
]
