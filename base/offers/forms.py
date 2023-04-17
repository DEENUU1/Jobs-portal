from django import forms
from .models import (
    Position,
    Level,
    Localization,
    Contract,


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


class LocalizationFilterForm(forms.Form):
    localization = forms.ModelChoiceField(
        queryset=Localization.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose localization"
    )


class ContractFilterForm(forms.Form):
    contract = forms.ModelChoiceField(
        queryset=Contract.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose contract"
    )