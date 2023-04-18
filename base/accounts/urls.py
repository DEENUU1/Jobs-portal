from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('dashboard/', views.CompanyDashboard.as_view(), name='dashboard'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_profile'),

]