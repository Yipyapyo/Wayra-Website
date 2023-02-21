"""Forms to input investment between an investor and a startup"""
from django import forms
from portfolio.models.investment_model import Investment
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.models.investor_company_model import InvestorCompany


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['investor', 'startup', 'typeOfFoundingRounds', 'moneyRaised', 'dateInvested']

        investor = forms.ModelMultipleChoiceField(
            label="Select the investors in this investment",
            widget=forms.CheckboxSelectMultiple,
            queryset=InvestorIndividual.objects.all().union(InvestorCompany.objects.all())
        )
