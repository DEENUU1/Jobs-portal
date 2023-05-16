from typing import Any, Dict

from django.db.models import QuerySet
from django.views.generic import ListView

from .forms import DateSortingForm, ChooseCategoriesForm
from .models import Resources


class StudyHomePageListView(ListView):
    """
    A class-based view for displaying a list of study resources on the homepage.
    Attributes:
        model (django.db.models.Model): The model to use for the list view.
        template_name (str): The name of the template to render for the view.
        paginate_by (int): The number of items to display per page.
    Methods:
        get_queryset(): Retrieves the queryset for the view and applies filtering based on user input.
        get_context_data(): Adds additional context data to be passed to the template.
    """

    model = Resources
    template_name = "study_home_page_list.html"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """
        Retrieves the queryset for the view and applies filtering based on user input.
        Returns:
            django.db.models.QuerySet: The queryset to use for the view.
        """
        queryset = super().get_queryset()

        order_by = self.request.GET.get("order_by")
        if order_by:
            if order_by == "1":
                queryset = queryset.order_by("date_created")
            if order_by == "2":
                queryset = queryset.order_by("-date_created")

        categories = self.request.GET.get("choose_categories")
        if categories:
            queryset = queryset.filter(category__in=categories)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Adds additional context data to be passed to the template.
        Args:
            **kwargs: Arbitrary keyword arguments.
        Returns:
            dict: A dictionary of context data to pass to the template.
        """
        context = super().get_context_data(**kwargs)
        context["date_sorting_form"] = DateSortingForm(self.request.GET)
        context["filter_by_categories"] = ChooseCategoriesForm(self.request.GET)

        return context
