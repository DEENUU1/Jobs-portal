from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import login


class RegisterUserView(FormView):
    template_name = "register_user.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class LoginUserView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


def home(request):
    return render(
        request, "home.html", {'user': request.user}
    )
