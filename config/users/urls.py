from django.urls import path


from . import views

app_name = 'users'

urlpatterns = [
    path('sign-in/', views.UserLoginView.as_view(), name='login'),
    path('sing-out/', views.UserLogoutView.as_view(), name='logout'),
    path('sign-up/', views.UserRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
