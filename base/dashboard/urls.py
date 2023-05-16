from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("offer/edit/<int:pk>/", views.OfferUpdateView.as_view(), name="edit-offer"),
    path("offer/create/", views.OfferCreateView.as_view(), name="create-offer"),
    path(
        "offer/delete/<int:pk>/", views.OfferDeleteView.as_view(), name="delete-offer"
    ),
    path(
        "application/<int:offer_id>/",
        views.ApplicationsListView.as_view(),
        name="applications",
    ),
    path(
        "application/send-feedback/<int:application_id>/",
        views.ReturnApplicationFeedbackView.as_view(),
        name="send-feedback",
    ),
    path(
        "application/delete/<int:pk>/",
        views.ApplicationDeleteView.as_view(),
        name="delete-application",
    ),
    path(
        "application/generate-csv/<int:pk>/",
        views.generate_application_csv,
        name="generate-csv",
    ),
    path("dashboard/", views.CompanyDashboard.as_view(), name="dashboard"),
]
