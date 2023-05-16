from accounts.tasks import send_email_task
from django import forms


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
            self.cleaned_data["subject"],
            self.cleaned_data["message"],
        )
