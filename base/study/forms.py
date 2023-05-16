from django import forms
from django.forms import ModelMultipleChoiceField

from .models import Category


class DateSortingForm(forms.Form):
    """
    DateSortingForm is a Django form that provides a dropdown menu to select the order in which
    job offers are sorted by date.
    Attributes:
        - order_by (ChoiceField): A field that represents a dropdown menu selection of sorting order.
    """

    CHOICES = (("1", "Newest"), ("2", "Oldest"))

    order_by = forms.ChoiceField(
        choices=CHOICES,
        required=False,
    )


class ChooseCategoriesForm(forms.Form):
    """
    ChoosePositionsForm is a Django form that provides a checkbox for each available
    Categories object, allowing users to select which positions they are interested in.
    Attributes:
        - choose_positions (ModelMultipleChoiceField): A field that represents a multiple-choice selection of objects.
    """

    choose_categories = ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Choose positions",
    )
