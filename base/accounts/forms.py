from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser
from .tasks import send_email_task


class CustomUserForm(forms.ModelForm):
    """
    A form used for creating a new CustomUser account. The form includes fields for username, email and password,
    as well as additional fields for role, first name, and last name.

    Attributes:
        username: A CharField containing the username of the user.
        email: An EmailField containing the email address of the user.
        password: A CharField containing the password of the user.
    """
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
        """
        A method to validate if the provided email already exists in
        CustomUser database, and raises a validation error if it does.
        """
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    def send_email(self, message):
        """
        A method that sends an activation email to the user's provided email address, using an asynchronous task.
        """
        send_email_task.delay(
            self.cleaned_data['email'],
            subject="Activate your account",
            message=message
        )


class LoginForm(AuthenticationForm):
    """
    A form used for authenticating a user. The form inherits from the built-in AuthenticationForm and includes
    fields for username and password, with custom styling for the widgets.
    Attributes:
        username: A CharField containing the username of the user.
        password: A CharField containing the password of the user.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ChangePasswordForm(forms.Form):
    """
    A form used for changing the password of a user. The form includes fields for email, old password, and new password.
    Attributes:
        email: An EmailField containing the email address of the user.
        old_password: A CharField containing the old password of the user.
        new_password: A CharField containing the new password of the user.
    """
    email = forms.EmailField(widget=forms.EmailInput)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)


class ReturnApplicationFeedbackForm(forms.Form):
    """
    A form used for receiving feedback from users. The form includes fields for email, subject, and message.
    Attributes:
        email: An EmailField containing the email address of the user.
        subject: A CharField containing the subject of the feedback message.
        message: A CharField containing the feedback message.
    """
    email = forms.EmailField(widget=forms.EmailInput)
    subject = forms.CharField(widget=forms.TextInput)
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self, email):
        """
        A method that sends an email to the provided email address,
        containing the feedback message and subject, using an asynchronous task.
        """
        send_email_task.delay(
            email,
            self.cleaned_data['subject'],
            self.cleaned_data['message'],
        )
