from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django import views
from django.utils.decorators import method_decorator
from .auth import company_required, user_required
from .models import CustomUser
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import QuerySet
from offers.models import Offer, Application
from typing import Any , Dict


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

        return render(request,
                      'user_profile.html',
                      )


class ApplicationsListView(ListView):
    model = Application
    paginate_by = 20
    template_name = 'applications_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(offer__company=self.kwargs['offer_id'])
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class OfferDeleteView(DeleteView):
    model = Offer
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
        return queryset


class OfferCreateView(CreateView):
    model = Offer
    fields = [
        'name', 'description', 'level', 'requirements', 'localization',
        'contract', 'position', 'salary_from', 'salary_to', 'remote'
    ]
    template_name = 'offer_create.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.id)
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