from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import CustomUserForm


class RegisterUserView(FormView):
    template_name = "register_user.html"
    form_class = CustomUserForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def home(request):
    return render(
        request, "home.html", {}
    )
