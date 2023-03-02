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

    def __init__(self, *args, **kwargs):
        super(InvestorCompanyCreateForm, self).__init__(*args, **kwargs)
    #investors = InvestorCompany.objects.all().values_list('company__id', flat=True)
    company = CompanyChoiceField(
        queryset = Company.objects.filter(~Exists(InvestorCompany.objects.filter(company=OuterRef('id')))),
        #queryset = Company.objects.exclude(id__in=investors),
        widget=forms.Select()
    )
    

class InvestorCompanyEditForm(forms.ModelForm):
    class Meta:
        model = InvestorCompany
        fields = ["angelListLink", "crunchbaseLink", "linkedInLink", "classification"]
    
