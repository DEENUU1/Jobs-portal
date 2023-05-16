from django.urls import path

from . import views

app_name = "study"

urlpatterns = [
    path("", views.StudyHomePageListView.as_view(), name="study_list"),
]
