"""Forms to create investor individual."""
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from portfolio.models.investor_individual_model import InvestorIndividual


class InvestorIndividualForm(forms.ModelForm):
    """Forms to create investor individual."""

    class Meta:
        model = InvestorIndividual
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InvestorIndividualForm, self).__init__(*args, **kwargs)
        self.fields['PrimaryNumber'].widget = PhoneNumberPrefixWidget()
        self.fields['SecondaryNumber'].widget = PhoneNumberPrefixWidget()
