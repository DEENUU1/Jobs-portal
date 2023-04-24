from django import forms


class DateSortingForm(forms.Form):
    """
    DateSortingForm is a Django form that provides a dropdown menu to select the order in which
    job offers are sorted by date.
    Attributes:
        - order_by (ChoiceField): A field that represents a dropdown menu selection of sorting order.
    """
    CHOICES = (
        ("1", "Newest"),
        ("2", "Oldest")
    )

    order_by = forms.ChoiceField(
        choices=CHOICES,
        required=False,
    )
