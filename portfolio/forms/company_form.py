"""Forms for the VC portfolio management site"""
from django import forms
from portfolio.models import Company


# Form for creating an individual / client
class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "company_registration_number", "trading_names",
                  "previous_names", "registered_address", "jurisdiction"]

    def __init__(self, *args, **kwargs):
        super(CompanyCreateForm, self).__init__(*args, **kwargs)