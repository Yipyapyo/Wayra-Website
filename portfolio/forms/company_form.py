"""Forms for the VC portfolio management site"""
from django import forms
from portfolio.models import Company, InvestorCompany, Investment
from django.db.models import Exists, OuterRef


# Form for creating an individual / client
class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_registration_number", "trading_names",
                  "previous_names", "registered_address", "jurisdiction"]

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)


class CompanyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

# Form for setting company as investor company 
class InvestorCompanyCreateForm(forms.ModelForm):
    class Meta:
        model = InvestorCompany
        fields = ["company", "angelListLink", "crunchbaseLink", "linkedInLink", "classification"]

    company = CompanyChoiceField(
        queryset = Company.objects.filter(~Exists(Investment.objects.filter(investor=OuterRef('pk')))),
        widget = forms.Select()
    )

class InvestorCompanyEditForm(forms.ModelForm):
    class Meta:
        model = InvestorCompany
        fields = ["angelListLink", "crunchbaseLink", "linkedInLink", "classification"]
    
