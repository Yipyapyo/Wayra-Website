"""Forms for the VC portfolio management site"""
from django import forms
from portfolio.models import Company, Portfolio_Company
from django.db.models import Exists, OuterRef


# Form for creating an individual / client
class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_registration_number", "trading_names",
                  "previous_names", "registered_address", "jurisdiction"]

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)

class ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class PortfolioCompanyCreateForm(forms.ModelForm):
    class Meta: 
        model = Portfolio_Company
        fields = ["parent_company", "wayra_number"]
    
    parent_company = ModelChoiceField(
        queryset=Company.objects.filter(~Exists(Portfolio_Company.objects.filter(parent_company=OuterRef('id')))),
        widget=forms.Select()
    )