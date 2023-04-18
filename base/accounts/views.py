from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django import views
from django.utils.decorators import method_decorator
from .auth import company_required
from offers.models import Offer, Application


class RegisterUserView(FormView):
    template_name = "register_user.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("offers:home")

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class LoginUserView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("offers:home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


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