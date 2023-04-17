from django import forms
from .models import (
    Position,
)
from django.forms import ModelMultipleChoiceField


class ChoosePositionsForm(forms.Form):
    choose_positions = ModelMultipleChoiceField(   
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Choose positions"
    )
