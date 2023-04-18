from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Offer, Application
from typing import Any , Dict 
from django.db.models import QuerySet
from .forms import (
    ChoosePositionsForm,
    LevelFilterForm, 
    LocalizationFilterForm, 
    ContractFilterForm,
    DateSortingForm,
    SearchForm,
    RemoteFilterForm,

)    
from accounts.models import CustomUser


class HomePageView(ListView):
    model = Offer
    template_name = 'home_page.html'
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()

        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        remote = self.request.GET.get('remote')
        if remote:
            queryset = queryset.filter(remote=True)

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

        order_by = self.request.GET.get('order_by')
        if order_by:
            if order_by == "1":
                queryset = queryset.order_by('date_created')
            if order_by == "2":
                queryset = queryset.order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)            

        context['positions_form'] = ChoosePositionsForm(self.request.GET)
        context['level_form'] = LevelFilterForm(self.request.GET)
        context['localization_form'] = LocalizationFilterForm(self.request.GET)
        context['contract_form'] = ContractFilterForm(self.request.GET)
        context['date_sorting_form'] = DateSortingForm(self.request.GET)
        context['search_form'] = SearchForm(self.request.GET)
        context['remote_form'] = RemoteFilterForm(self.request.GET)

        return context


class OfferDetailView(DetailView):
    model = Offer
    template_name = 'offer_detail.html'


class OfferUpdateView(UpdateView):
    model = Offer
    fields = ['name', 'description', 'level', 'localization', 'contract', 'position', 'salary_from', 'salary_to', 'remote']
    template_name = 'offer_update.html'
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class OfferCreateView(CreateView):
    model = Offer
    fields = ['name', 'description', 'level', 'requirements', 'localization', 'contract', 'position', 'salary_from', 'salary_to', 'remote']
    template_name = 'offer_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class OfferDeleteView(DeleteView):
    model = Offer
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class CompaniesListView(ListView):
    model = CustomUser
    paginate_by = 10
    template_name = 'companies_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(role='company')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)            
        return context
    

class CompanyDetailView(DetailView):
    model = CustomUser
    template_name = 'company_detail.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(role='company')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)    
        context['object_list'] = Offer.objects.filter(company=self.kwargs['pk'])        
        return context
    

class ApplyForOfferView(CreateView):
    model = Application
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'message', 'expected_pay', 'portfolio', 'linkedin', 'cv']
    template_name = 'apply_for_offer.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.offer_id = self.kwargs['offer_id']
        return super().form_valid(form)


class ApplicationsListView(ListView):
    model = Application
    paginate_by = 20
    template_name = 'applications_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context