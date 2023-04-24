from typing import Any, Dict
from django.db.models import QuerySet
from django.views.generic import ListView
from .models import Category, Resources
from .forms import DateSortingForm


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

        order_by = self.request.GET.get('order_by')
        if order_by:
            if order_by == "1":
                queryset = queryset.order_by('date_created')
            if order_by == "2":
                queryset = queryset.order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """

        """
        context =super().get_context_data(**kwargs)
        context['date_sorting_form'] = DateSortingForm(self.request.GET)

        return context
