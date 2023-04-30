import csv
from typing import Any, Dict

from accounts.auth import company_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, FormView, DeleteView, UpdateView, View

from .forms import (
    ReturnApplicationFeedbackForm,

)
from .models import Offer, Application


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


class CompanyDashboard(View):
    """
    The class CompanyDashboard extends the built-in Django View class
    and is used to display a dashboard for a company user.
    """
    @method_decorator(company_required)
    def get(self, request, *args, **kwargs):
        """
        Retrieves the company ID from the logged-in user's request,
        filters the offers that belong to that company, counts the number of applications for those offers,
        and returns a rendered dashboard template with the retrieved data.
        """
        company_id = request.user.id
        offers = Offer.objects.filter(company_id=company_id)
        applications_count = Application.objects.filter(offer_id__in=offers).count()

        context = {
            'company':  company_id,
            'offers': offers,
            'applications_count': applications_count
        }
        return render(request,
                      'company_dashboard.html',
                      context=context
                      )