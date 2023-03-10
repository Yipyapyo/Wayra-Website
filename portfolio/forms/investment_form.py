"""Forms to input investment between an investor and a startup"""
from django import forms
from portfolio.models.investment_model import Investment, Investor, ContractRight
from portfolio.models.company_model import Portfolio_Company, Company


class InvestorChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.company is not null:
            return obj.company.name
        else:
            return obj.individual.name


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
        queryset=Investor.objects.all(),
        widget=forms.Select()
    )

    startup = StartupChoiceField(
        queryset=Portfolio_Company.objects.all(),
        widget=forms.Select()
    )


class ContractRightForm(forms.ModelForm):
    class Meta:
        model = ContractRight
        fields = ["right", "details"]

    right_investment = None

    def saveInvestment(self, invest):
        self.right_investment = invest

    def save(self):
        super().save(commit=False)
        ContractRight.objects.create(
            investment=self.right_investment,
            right=self.cleaned_data.get("right"),
            details=self.cleaned_data.get("details")
        )
