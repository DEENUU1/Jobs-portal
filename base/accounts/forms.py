from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


class CustomUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = (
            'role',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ChangePasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)