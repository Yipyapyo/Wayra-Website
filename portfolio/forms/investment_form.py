"""Forms to input investment between an investor and a startup"""
from django import forms
from portfolio.models.investment_model import Investment
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.company_model import Portfolio_Company


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = []
