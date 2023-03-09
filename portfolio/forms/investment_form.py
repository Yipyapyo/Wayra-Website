"""Forms to input investment between an investor and a startup"""
from django import forms
from portfolio.models.investment_model import Investment
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.company_model import Portfolio_Company


class InvestorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.company.name


class StartupChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ["investor", "startup", "typeOfFoundingRounds", "investmentAmount", "dateInvested"]
        widgets = {
            'dateInvested': forms.DateInput(attrs={
                'type': 'date'
            }),
        }

    investor = InvestorChoiceField(
        queryset=InvestorCompany.objects.all(),
        widget=forms.Select()
    )

    startup = StartupChoiceField(
        queryset=Portfolio_Company.objects.all(),
        widget=forms.Select()
    )
