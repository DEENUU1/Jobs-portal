from typing import Any, Dict

from accounts.models import CustomUser
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .report import calculate_avg_rating

from .forms import (
    ChoosePositionsForm,
    LevelFilterForm,
    LocalizationFilterForm,
    ContractFilterForm,
    DateSortingForm,
    SearchForm,
    RemoteFilterForm,

)
from .models import Offer, Application


class HomePageView(ListView):
    """
    This module defines a class called HomePageView which is a subclass of the built-in ListView class.
    This view renders a template 'home_page.html' and displays a paginated list of Offer objects.
    Attributes:
        - model (Offer): The model that the view is based on.
        - template_name (str): The name of the template that will be used to render the view.
        - paginate_by (int): The number of objects to display per page.
    """
    model = Offer
    template_name = 'home_page.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        """
        Returns the queryset that will be used to display the list of objects on the page.
        It filters the queryset based on the GET parameters that are passed with the request, such as:
        name, remote, choose_positions, level, localization, contract and order_by.
        """
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
        """
        Returns the context data that will be used to render the template.
        It adds different forms for filtering and searching the queryset to the context data.
        """
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
    """
    This module defines a class called OfferDetailView which is a subclass of the built-in DetailView class.
    This view renders a template 'offer_detail.html' and displays the details of a single Offer object.
    Attributes:
        - model (Offer): The model that the view is based on.
        - template_name (str): The name of the template that will be used to render the view.
    """
    model = Offer
    template_name = 'offer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.object.company
        avg_rating = calculate_avg_rating(company)
        context['avg_rating'] = avg_rating
        return context


class CompaniesListView(ListView):
    """
    This module defines a class called CompaniesListView which is a subclass of the built-in ListView class.
    This view renders a template 'companies_list.html' and displays a paginated list of CustomUser objects that
    have a role of 'company'.
    Attributes:
        - model (CustomUser): The model that the view is based on.
        - paginate_by (int): The number of objects to display per page.
        - template_name (str): The name of the template that will be used to render the view.
    """
    model = CustomUser
    paginate_by = 10
    template_name = 'companies_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        """
        Returns the queryset that will be used to display the list of objects on the page.
        It filters the queryset to only include objects with a role of 'company'.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(role='company')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Returns the context data that will be used to render the template.
        """
        context = super().get_context_data(**kwargs)            
        return context
    

class CompanyDetailView(DetailView):
    """
    This module defines a class called CompanyDetailView which is a subclass of the built-in DetailView class.
    This view renders a template 'company_detail.html' and displays the details of a single CustomUser object that
    has a role of 'company'. Additionally, it includes a list of related Offer objects.
    Attributes:
        - model (CustomUser): The model that the view is based on.
        - template_name (str): The name of the template that will be used to render the view.
    """
    model = CustomUser
    template_name = 'company_detail.html'

    def get_queryset(self) -> QuerySet[Any]:
        """
        Returns the queryset that will be used to display the object details.
        It filters the queryset to only include objects with a role of 'company'.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(role='company')
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Returns the context data that will be used to render the template.
        It adds the related Offer objects to the context data.
        """
        context = super().get_context_data(**kwargs)    
        avg_rating = calculate_avg_rating(self.object)
        context['object_list'] = Offer.objects.filter(company=self.kwargs['pk'])
        context['avg_rating'] = avg_rating
        return context
    

class ApplyForOfferView(CreateView):
    """
    This module defines a class called ApplyForOfferView which is a subclass of the built-in CreateView class.
    This view is used to handle the form submission for a job application.
    Attributes:
        - model (Application): The model that the view is based on.
        - fields (list): The list of fields that will be included in the form.
        - template_name (str): The name of the template that will be used to render the view.
        - success_url (str): The URL to redirect to upon successful submission of the form.
    """
    model = Application
    fields = [
        'first_name', 'last_name', 'email', 'phone_number', 'message', 'expected_pay', 'portfolio', 'linkedin', 'cv'
    ]
    template_name = 'apply_for_offer.html'
    success_url = reverse_lazy("offers:apply-success")

    def form_valid(self, form):
        """
        Called when the form is submitted with valid data. This method saves the form data to the database
        and sets the offer_id to the value passed in the URL parameters. It returns an HTTP response to the success URL.
        """
        form.instance.offer_id = self.kwargs['offer_id']
        return super().form_valid(form)


class ApplySuccessView(TemplateView):
    """
    This module defines a class called ApplySuccessView which is a subclass of the built-in TemplateView class.
    This view is used to render a success page upon successful submission of a job application.
    Attributes:
        - template_name (str): The name of the template that will be used to render the view.
    """
    template_name = 'apply_success.html'
