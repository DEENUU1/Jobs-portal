from dashboard.models import Application
from django import views
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, TemplateView
from django.views.generic.edit import FormView
from dotenv import load_dotenv
from offers.models import CustomUser

from .auth import user_required
from .forms import CustomUserForm, LoginForm, ChangePasswordForm
from .tokens import account_activation_token

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
            message=render_to_string('auth/acc_active_email.html', {
                'user': user,
                'domain': get_current_site(self.request),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        )
        return super().form_valid(form)


def register_activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
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
