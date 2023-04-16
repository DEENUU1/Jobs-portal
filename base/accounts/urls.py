from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),

]