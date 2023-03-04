from django import forms
from portfolio.models.investor_individual_model import InvestorIndividual
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class InvestorIndividualForm(forms.ModelForm):
    class Meta:
        model = InvestorIndividual
        fields = '__all__'

    def __init__(self, *args, **kwargs):
       super(InvestorIndividualForm, self).__init__(*args, **kwargs)
       self.fields['PrimaryNumber'].widget = PhoneNumberPrefixWidget()
       self.fields['SecondaryNumber'].widget = PhoneNumberPrefixWidget()
    