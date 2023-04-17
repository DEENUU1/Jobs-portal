from django.views.generic import ListView
from .models import Offer
from typing import Any , Dict 
from django.db.models import QuerySet
from .forms import (
    ChoosePositionsForm,
    LevelFilterForm, 
    LocalizationFilterForm, 
    ContractFilterForm,


)    
from accounts.models import CustomUser


class HomePageView(ListView):
    model = Offer
    template_name = 'home_page.html'
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        positions = self.request.GET.getlist('choose_positions')
        if positions:
            queryset = queryset.filter(position__in=positions)

        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)

        localization = self.request.GET.get('localization')
        if localization:
            queryset = queryset.filter(localization=localization)

        contract = self.request.GET.get('contract')
        if contract:
            queryset = queryset.filter(contract=contract)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)            

        context['positions_form'] = ChoosePositionsForm(self.request.GET)
        context['level_form'] = LevelFilterForm(self.request.GET)
        context['localization_form'] = LocalizationFilterForm(self.request.GET)
        context['contract_form'] = ContractFilterForm(self.request.GET)
        
        return context
    

class CompaniesListView(ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'companies_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(role='company')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)            
        return context