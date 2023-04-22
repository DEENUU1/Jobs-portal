from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserForm, LoginForm, ChangePasswordForm, ReturnApplicationFeedbackForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django import views
from django.utils.decorators import method_decorator
from .auth import company_required, user_required
from .models import CustomUser
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import QuerySet
from offers.models import Offer, Application
from typing import Any , Dict
from dotenv import load_dotenv
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.http import HttpResponse
from .tasks import generate_csv_file


load_dotenv()


class RegisterUserView(FormView):
    template_name = "register_user.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("accounts:success_register")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        user.set_password(form.cleaned_data['password'])
        user.save()
        form.send_email(
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': get_current_site(self.request),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
        )
        return super().form_valid(form)

def register_activate(request, uidb64, token):
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
    template_name = "register_success.html"


class LoginUserView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("offers:home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = "change_password.html"
    success_url = reverse_lazy("accounts:success_password_change")

    def form_valid(self, form):
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
    template_name = "password_change_success.html"



class LogoutUser(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('offers:home')


class CompanyDashboard(views.View):

    @method_decorator(company_required)
    def get(self, request, *args, **kwargs):
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


class ProfileUpdateView(UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'description', 'image', 'username']
    template_name = 'profile_update.html'
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.request.user.id)
        return queryset


class UserProfileView(views.View):

    @method_decorator(user_required)
    def get(self, request, *args, **kwargs):
        user_id = request.user.email
        applications = Application.objects.filter(email=user_id)

        context = {
            'applications': applications
        }

        return render(request,
                      'user_profile.html',
                      context=context
                      )


class ApplicationsListView(UserPassesTestMixin, ListView):
    model = Application
    paginate_by = 20
    template_name = 'applications_list.html'

    def test_func(self):
        return self.request.user.role == "company"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        # queryset = queryset.filter(offer__company=self.kwargs['offer_id'])
        queryset = queryset.filter(offer__id=self.kwargs['offer_id'])
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class ReturnApplicationFeedbackView(UserPassesTestMixin, FormView):
    form_class = ReturnApplicationFeedbackForm
    template_name = "return_app_feedback.html"
    success_url = reverse_lazy("offers:home")

    def test_func(self):
        application = Application.objects.get(pk=self.kwargs['application_id'])
        offer = application.offer
        return self.request.user.role == "company" and self.request.user == offer.company

    def get_initial(self):
        initial = super().get_initial()
        application = Application.objects.get(pk=self.kwargs['application_id'])
        initial['email'] = application.email
        return initial

    def form_valid(self, form):
        application = Application.objects.get(pk=self.kwargs['application_id'])
        email = application.email
        form.send_email(email)
        application.update_answer(True)
        return super().form_valid(form)


class ApplicationDeleteView(DeleteView):
    model = Application
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs['pk'])
        return queryset


class OfferDeleteView(DeleteView):
    model = Offer
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class OfferCreateView(UserPassesTestMixin, CreateView):
    model = Offer
    fields = [
        'name', 'description', 'level', 'requirements', 'localization',
        'contract', 'position', 'salary_from', 'salary_to', 'remote'
    ]
    template_name = 'offer_create.html'
    success_url = "/"

    def test_func(self):
        return self.request.user.role == "company"

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user)
        return queryset


class OfferUpdateView(UpdateView):
    model = Offer
    fields = [
        'name', 'description', 'level', 'localization', 'contract', 'position', 'salary_from', 'salary_to', 'remote'
    ]
    template_name = 'offer_update.html'
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


def generate_application_csv(request, pk):
    generate_csv_file.apply_async(args=[pk])
    return HttpResponse('CSV generation started. You will receive a download link shortly.')