from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', views.register_activate, name='activate'),
    path('register/success', views.SuccessRegisterView.as_view(), name='success_register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change-password/success', views.SuccessPasswordChangeView.as_view(), name='success_password_change'),
    path('dashboard/', views.CompanyDashboard.as_view(), name='dashboard'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('offer/edit/<int:pk>/', views.OfferUpdateView.as_view(), name='edit'),
    path('offer/create/', views.OfferCreateView.as_view(), name='create'),
    path('offer/delete/<int:pk>/', views.OfferDeleteView.as_view(), name='delete'),
    path('applications/<int:offer_id>/', views.ApplicationsListView.as_view(), name='applications'),
    path('application/sendfeedback/<int:application_id>/', views.ReturnApplicationFeedbackView.as_view(), name='send_feedback'),
    path('application/delete/<int:pk>/', views.ApplicationDeleteView.as_view(), name='delete_application'),
    path('application/generate-csv/<int:pk>/', views.generate_application_csv, name='generate_csv'),

]