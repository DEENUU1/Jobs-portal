from typing import Any, Dict
import csv
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import CustomUser, CompanyReview
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, DeleteView, UpdateView
from .report import calculate_avg_rating

from .forms import (
    ChoosePositionsForm,
    LevelFilterForm,
    LocalizationFilterForm,
    ContractFilterForm,
    DateSortingForm,
    SearchForm,
    RemoteFilterForm,
    ReturnApplicationFeedbackForm,

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
        context['reviews'] = CompanyReview.objects.filter(company=self.kwargs['pk'])
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


class ApplicationsListView(UserPassesTestMixin, ListView):
    """
    The ApplicationsListView class is a ListView that displays a list of job applications for a specific job offer.
    It extends the UserPassesTestMixin to restrict access to the view to users with the "company" role.
    Attributes:
        - model: The model class to use for this view (Application).
        - paginate_by: The number of items to include in each page of results.
        - template_name: The name of the template to use for rendering the view.
    """
    model = Application
    paginate_by = 20
    template_name = 'applications_list.html'

    def test_func(self):
        """
        Overrides the UserPassesTestMixin test_func to check if the logged-in user has the "company" role.
        """
        return self.request.user.role == "company"

    def get_queryset(self) -> QuerySet[Any]:
        """
        Overrides the parent get_queryset method to filter the queryset by the job offer ID specified in the URL.
        """
        queryset = super().get_queryset()
        # queryset = queryset.filter(offer__company=self.kwargs['offer_id'])
        queryset = queryset.filter(offer__id=self.kwargs['offer_id'])
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Overrides the parent get_context_data method to add any additional context data required by the template.
        """
        context = super().get_context_data(**kwargs)
        return context


class ReturnApplicationFeedbackView(UserPassesTestMixin, FormView):
    """
    ReturnApplicationFeedbackView is a view that allows a company user to provide feedback on a particular
    job application. The user must be authenticated and have the role of 'company' to access this view.
    Attributes:
        - form_class (ReturnApplicationFeedbackForm): A form used for the feedback input.
        - template_name (str): A string representing the HTML template to be rendered.
        - success_url (reverse_lazy): A URL to redirect to after successfully submitting the feedback.
    """
    form_class = ReturnApplicationFeedbackForm
    template_name = "return_app_feedback.html"
    success_url = reverse_lazy("offers:home")

    def test_func(self):
        """
        A function that checks whether the logged in user is a company user and is associated
        with the offer for the application in question.
        """
        application = Application.objects.get(pk=self.kwargs['application_id'])
        offer = application.offer
        return self.request.user.role == "company" and self.request.user == offer.company

    def get_initial(self):
        """
        A function that pre-populates the feedback form with the email address of the applicant.
        """
        initial = super().get_initial()
        application = Application.objects.get(pk=self.kwargs['application_id'])
        initial['email'] = application.email
        return initial

    def form_valid(self, form):
        """
        A function that sends an email with the feedback to the applicant and updates the application status
        to reflect the feedback was returned.
        """
        application = Application.objects.get(pk=self.kwargs['application_id'])
        email = application.email
        form.send_email(email)
        application.update_answer(True)
        return super().form_valid(form)


class ApplicationDeleteView(DeleteView):
    """
    ApplicationDeleteView is a view that allows a user to delete a specific job application.
    Attributes:
        - model (Application): The model associated with this view, used to retrieve the application instance to be deleted.
        - success_url (str): The URL to redirect to after successfully deleting the application.
    """
    model = Application
    success_url = "/"

    def get_queryset(self):
        """
        A function that retrieves the queryset used for this view.
        It filters the queryset to only include the application with the primary key specified in the URL.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs['pk'])
        return queryset


class OfferDeleteView(DeleteView):
    """
    OfferDeleteView is a view that allows a company user to delete one of their job offers.
    Attributes:
        - model (Offer): The model associated with this view, used to retrieve the offer instance to be deleted.
        - success_url (str): The URL to redirect to after successfully deleting the offer.
    """
    model = Offer
    success_url = "/"

    def get_queryset(self):
        """
        A function that retrieves the queryset used for this view.
        It filters the queryset to only include the offer instances owned by the logged in company user.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class OfferCreateView(UserPassesTestMixin, CreateView):
    """
    OfferCreateView is a view that allows a company user to create a new job offer.
    Attributes:
        - model (Offer): The model associated with this view, used to create a new offer instance.
        - fields (list): A list of strings representing the form fields to be displayed.
        - template_name (str): A string representing the HTML template to be rendered.
        - success_url (str): The URL to redirect to after successfully creating the offer.
    """
    model = Offer
    fields = [
        'name', 'description', 'level', 'requirements', 'localization',
        'contract', 'position', 'salary_from', 'salary_to', 'remote'
    ]
    template_name = 'offer_create.html'
    success_url = "/"

    def test_func(self):
        """
        A function that checks whether the logged-in user is a company user.
        """
        return self.request.user.role == "company"

    def form_valid(self, form):
        """
        A function that assigns the logged in company user as the owner of the offer instance.
        """
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        """
        A function that retrieves the queryset used for this view.
        It filters the queryset to only include the offer instances owned by the logged in company user.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user)
        return queryset


class OfferUpdateView(UpdateView):
    """
    OfferUpdateView is a view that allows a company user to update one of their existing job offers.
    Attributes:
        - model (Offer): The model associated with this view, used to retrieve the offer instance to be updated.
        - fields (list): A list of strings representing the form fields to be displayed.
        - template_name (str): A string representing the HTML template to be rendered.
        - success_url (str): The URL to redirect to after successfully updating the offer.
    """
    model = Offer
    fields = [
        'name', 'description', 'level', 'localization', 'contract', 'position', 'salary_from', 'salary_to', 'remote'
    ]
    template_name = 'offer_update.html'
    success_url = "/"

    def get_queryset(self):
        """
        A function that retrieves the queryset used for this view.
        It filters the queryset to only include the offer instances owned by the logged in company user.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


def generate_application_csv(request, pk):
    """
    View function that generates a CSV file of job applications for a specified job offer.
    Attributes:
        - request (HttpRequest): The HTTP request object.
        - pk (int): The primary key of the job offer.
    Returns:
        - HttpResponse: An HTTP response object.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full name', 'Email', 'Expected pay', 'Linkedin', 'Portfolio'])

    application = Application.objects.filter(offer__id=pk)

    for data in application:
        writer.writerow([data.return_full_name, data.email, data.expected_pay, data.linkedin, data.portfolio])

    return response
