from dashboard.models import (
    Position,
    Level,
    Localization,
    Contract,
    Application,
)
from django import forms
from django.forms import ModelMultipleChoiceField


class ChoosePositionsForm(forms.Form):
    """
    ChoosePositionsForm is a Django form that provides a checkbox for each available
    Position object, allowing users to select which positions they are interested in.
    Attributes:
        - choose_positions (ModelMultipleChoiceField): A field that represents a multiple-choice selection of objects.
    """

    choose_positions = ModelMultipleChoiceField(
        queryset=Position.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Choose positions",
    )


class LevelFilterForm(forms.Form):
    """
    LevelFilterForm is a Django form that provides a dropdown menu to select a Level object,
    used for filtering job offers by level.
    Attributes:
        - level (ModelChoiceField): A field that represents a dropdown menu selection of Level objects.
    """

    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose level",
    )


class LocalizationFilterForm(forms.Form):
    """
    LocalizationFilterForm is a Django form that provides a dropdown menu to select a Localization object,
    used for filtering job offers by location.
    Attributes:
        - localization (ModelChoiceField): A field that represents a dropdown menu selection of Localization objects.
    """

    localization = forms.ModelChoiceField(
        queryset=Localization.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose localization",
    )


class ContractFilterForm(forms.Form):
    """
    ContractFilterForm is a Django form that provides a dropdown menu to select a Contract object,
    used for filtering job offers by type of contract.
    Attributes:
        - contract (ModelChoiceField): A field that represents a dropdown menu selection of Contract objects.
    """

    contract = forms.ModelChoiceField(
        queryset=Contract.objects.all(),
        widget=forms.Select(),
        required=False,
        label="Choose contract",
    )


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


class RemoteFilterForm(forms.Form):
    """
    RemoteFilterForm is a Django form that provides a checkbox to filter job offers by remote work availability.
    Attributes:
        - remote (BooleanField): A field that represents a checkbox selection for remote work availability.
    """

    remote = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["remote"].label = "Remote"


class SearchForm(forms.Form):
    """
    A form used for searching offers by name.
    Fields:
        - name: a CharField for the search query, with an optional label and placeholder text.
    """

    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and overrides the default settings for the 'name' field.
        Parameters:
            - args: the positional arguments to be passed to the parent constructor.
            - kwargs: the keyword arguments to be passed to the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.fields["name"].required = False
        self.fields["name"].label = ""
        self.fields["name"].widget.attrs["placeholder"] = "Search by name"


class ApplyForm(forms.ModelForm):
    """
    The `ApplyForm` class is a Django ModelForm used to handle user input for creating or updating object.
    Attributes:
        - offer (IntegerField): A hidden input field that represents the id of the offer the user is applying for.
    Meta:
        - model (Application): The model to which the form is associated.
        - fields (str): The fields to include in the form. In this case, it includes all fields in model.
    """

    offer = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Application
        fields = "__all__"
