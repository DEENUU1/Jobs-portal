from typing import Any, Dict
from django.db.models import QuerySet
from django.views.generic import ListView
from .models import Category, Resources


class StudyHomePageListView(ListView):
    """

    """
    model = Resources
    template_name = 'study_home_page_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """

        """
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """

        """
        context =super().get_context_data(**kwargs)

        return context
