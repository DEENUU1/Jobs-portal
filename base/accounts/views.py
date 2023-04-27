import csv
from typing import Any, Dict

from django import views
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from dotenv import load_dotenv
from offers.models import Offer, Application

from .auth import company_required, user_required
from .forms import CustomUserForm, LoginForm, ChangePasswordForm, ReturnApplicationFeedbackForm
from .models import CustomUser, CompanyReview
from .tokens import account_activation_token
from django.http import Http404

load_dotenv()


class RegisterUserView(FormView):
    """
    A Django class-based view for registering new users.
    Attributes:
        template_name: A string containing the name of the template to be rendered for the registration form.
        form_class: A reference to the form class to be used for the registration form.
        success_url: A URL to redirect to upon successful user registration.
    """
    template_name = "auth/register_user.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("accounts:success_register")

    def form_valid(self, form):
        """
        A method that overrides the built-in form_valid method in the FormView class to handle successful
        form submissions.
        This method creates a new user instance, sets their password, saves the user with is_active set to False,
        sends an activation email to the user, and redirects to the success_url.
        """
        user = form.save(commit=False)
        user.is_active = False 
        user.set_password(form.cleaned_data['password'])
        user.save()
        form.send_email(
            message = render_to_string('auth/acc_active_email.html', {
                'user': user,
                'domain': get_current_site(self.request),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        )
        return super().form_valid(form)


def register_activate(request, uidb64, token):
    """
    The function register_activate() takes in three arguments:
    - request: the request object sent by the user to activate their account
    - idb64: the unique identifier in base64 encoded format
    - token: the token sent in the activation link
    The function attempts to decode the idb64 value and retrieve the corresponding user from the database.
    If the user is found and the token is valid, the user's account is activated, they are logged in,
    and a success message is returned. If the user is not found or the token is invalid, an error message is returned.
    Returns:
        - HttpResponse: A success or error message to be displayed to the user upon attempting to activate their account
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class SuccessRegisterView(TemplateView):
    """
    The class SuccessRegisterView extends the TemplateView class and is used to display a success message to the
    user after they have successfully registered for an account.
    """
    template_name = "auth/register_success.html"


class LoginUserView(FormView):
    """
    The class LoginUserView extends the FormView class and is used to authenticate a user's login credentials.
    Attributes:
        - template_name (str): The name of the template that will be rendered to display the login form.
        - form_class (Form): The class of the form that will be used to authenticate the user's login credentials.
        - success_url (str): The URL that the user will be redirected to upon successful authentication.
    """
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("offers:home")

    def form_valid(self, form):
        """
        Overrides the parent class method to log the user in upon successful
        authentication and redirect them to the success URL.
        """
        login(self.request, form.get_user())
        return super().form_valid(form)


class ChangePasswordView(FormView):
    """
    The class ChangePasswordView extends the FormView class and is used to change a user's password.
    Attributes:
        - form_class (Form): The class of the form that will be used to change the user's password.
        - template_name (str): The name of the template that will be rendered to display the change password form.
        - success_url (str): The URL that the user will be redirected to upon successful password change.
    """
    form_class = ChangePasswordForm
    template_name = "auth/change_password.html"
    success_url = reverse_lazy("accounts:success_password_change")

    def form_valid(self, form):
        """
        Overrides the parent class method to retrieve the user by their email, validate the old password,
        set and save the new password, and redirect the user to the success URL.
        """
        try:
            user = CustomUser.objects.get(email=form.cleaned_data['email'])
        except CustomUser.DoesNotExist:
            form.add_error(None, 'User with this email does not exist')
            return super().form_invalid(form)
        
        if not user.check_password(form.cleaned_data['old_password']):
            form.add_error('old_password', 'Old password is incorrect')
            return super().form_invalid(form)
        
        user.set_password(form.cleaned_data['new_password'])
        user.save()
        
        return super().form_valid(form)


class SuccessPasswordChangeView(TemplateView):
    """
    The class SuccessPasswordChangeView extends the TemplateView class and is used to display a success message
    to the user after they have successfully changed their password.
    Attributes:
        - template_name (str): The name of the template that will be rendered to display the success message.
    """
    template_name = "auth/password_change_success.html"


class LogoutUser(LogoutView):
    """
    The class LogoutUser extends the built-in Django LogoutView class and is used to log out the user from their account
    """
    def get(self, request):
        """
        Overrides the parent class method to log the user out and redirect them to the homepage URL.
        """
        logout(request)
        return redirect('offers:home')


class CompanyDashboard(views.View):
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
                      'profile/company_dashboard.html',
                      context=context
                      )


class ProfileUpdateView(UpdateView):
    """
    The class ProfileUpdateView extends the built-in Django UpdateView class
    and is used to allow a user to update their profile information.
    Attributes:
        - model (Model): The model that the view is updating.
        - fields (list): The list of fields that will be updated in the model.
        - template_name (str): The name of the template that will be rendered to display the update profile form.
        - success_url (str): The URL that the user will be redirected to upon successful profile update.
    """
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'description', 'image', 'username']
    template_name = 'profile/profile_update.html'
    success_url = "/"

    def get_queryset(self):
        """
        Overrides the parent class method to retrieve the queryset that contains only the logged-in user's information.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.request.user.id)
        return queryset


class UserProfileView(views.View):
    """
    The class UserProfileView extends the built-in Django View class
    and is used to display the user's profile information.
    """
    @method_decorator(user_required)
    def get(self, request, *args, **kwargs):
        """
        Retrieves the user's email from the logged-in user's request, filters the applications that
        belong to that user, and returns a rendered user profile template with the retrieved data.
        """
        user_id = request.user.email
        applications = Application.objects.filter(email=user_id)

        context = {
            'applications': applications
        }

        return render(request,
                      'profile/user_profile.html',
                      context=context
                      )


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


class AddCompanyReviewView(UserPassesTestMixin, CreateView):
    """

    """
    template_name = "add_company_review.html"
    success_url = reverse_lazy("offers:home")
    model = CompanyReview
    fields = ('email', 'choose_rate', 'short_description')

    def test_func(self):
        """

        """
        company = CustomUser.objects.get(pk=self.kwargs['company_id'])
        return company.role == "company"

    def get_initial(self):
        """

        """
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        initial['company'] = self.kwargs['company_id']
        return initial

    def form_valid(self, form):
        """

        """
        form.instance.company_id = self.kwargs['company_id']
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """

        """
        if not self.test_func():
            raise Http404
        return super().dispatch(request, *args, **kwargs)