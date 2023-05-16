from django.urls import path

from . import views

app_name = "offers"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("companies/", views.CompaniesListView.as_view(), name="companies-list"),
    path("offer/<int:pk>/", views.OfferDetailView.as_view(), name="offer-detail"),
    path("company/<int:pk>/", views.CompanyDetailView.as_view(), name="company-detail"),
    path(
        "apply/<int:offer_id>/", views.ApplyForOfferView.as_view(), name="apply-offer"
    ),
    path("apply/success", views.ApplySuccessView.as_view(), name="apply-success"),
    path(
        "company/add-review/<int:company_id>/",
        views.AddCompanyReviewView.as_view(),
        name="add-review",
    ),
]
