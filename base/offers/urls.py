from django.urls import path

from . import views

app_name = "offers"

urlpatterns = [
    path(
        '',
        views.HomePageView.as_view(),
        name='home'
    ),
    path(
        'companies/',
        views.CompaniesListView.as_view(),
        name='companies'
    ),
    path(
        'offer/<int:pk>/',
        views.OfferDetailView.as_view(),
        name='offer'
    ),
    path(
        'company/<int:pk>/',
        views.CompanyDetailView.as_view(),
        name='company'
    ),
    path(
        'apply/<int:offer_id>/',
        views.ApplyForOfferView.as_view(),
        name='apply'
    ),
    path(
        'apply/success',
        views.ApplySuccessView.as_view(),
        name='apply-success'
    ),
    path(
        'offer/edit/<int:pk>/',
        views.OfferUpdateView.as_view(),
        name='edit'
    ),
    path(
        'offer/create/',
        views.OfferCreateView.as_view(),
        name='create'
    ),
    path(
        'offer/delete/<int:pk>/',
        views.OfferDeleteView.as_view(),
        name='delete'
    ),
    path(
        'applications/<int:offer_id>/',
        views.ApplicationsListView.as_view(),
        name='applications'
    ),
    path(
        'application/sendfeedback/<int:application_id>/',
        views.ReturnApplicationFeedbackView.as_view(),
        name='send_feedback'
    ),
    path(
        'application/delete/<int:pk>/',
        views.ApplicationDeleteView.as_view(),
        name='delete_application'
    ),
    path(
        'application/generate-csv/<int:pk>/',
        views.generate_application_csv,
        name='generate_csv'
    ),

]