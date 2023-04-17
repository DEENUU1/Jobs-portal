from django import forms
from .models import (
    Position,
    Level,

)
from django.forms import ModelMultipleChoiceField


class ChoosePositionsForm(forms.Form):
    choose_positions = ModelMultipleChoiceField(   
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Choose positions"
    )


class LevelFilterForm(forms.Form):
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose level"
    )