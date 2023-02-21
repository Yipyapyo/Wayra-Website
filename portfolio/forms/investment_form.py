"""Forms to input investment between an investor and a startup"""
from django import forms
from portfolio.models.investment_model import Investment
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.company_model import PortfolioCompany


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['investor', 'individualInvestor', 'startup', 'typeOfFoundingRounds', 'moneyRaised']

        investor = forms.ModelMultipleChoiceField(
            label="Select the investors in this investment",
            widget=forms.CheckboxSelectMultiple,
            queryset=InvestorCompany.objects.all()
        )

        individualInvestor = forms.ModelMultipleChoiceField(
            label="Select the individual investor in this investment if there is one",
            widget=forms.CheckboxSelectMultiple,
            queryset=InvestorIndividual.objects.all()
        )

        startup = forms.ModelMultipleChoiceField(
            label="Select the portfolio company invested if there is one",
            widget=forms.CheckboxSelectMultiple,
            queryset=PortfolioCompany.objects.all()
        )
