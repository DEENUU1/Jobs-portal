from django.urls import path
from . import views

app_name = "offers"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('companies/', views.CompaniesListView.as_view(), name='companies'),
    path('offer/<int:pk>/', views.OfferDetailView.as_view(), name='offer'),
    

]