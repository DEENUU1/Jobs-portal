from django.views.generic import ListView
from .models import Offer
from typing import Any , Dict 
from django.db.models import QuerySet
from .forms import ChoosePositionsForm


class HomePageView(ListView):
    model = Offer
    paginate_by = 10
    template_name = 'home_page.html'
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        positions = self.request.GET.getlist('choose_positions')
        if positions:
            queryset = queryset.filter(position__in=positions)
            
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)            

        context['positions_form'] = ChoosePositionsForm(self.request.GET)

        return context