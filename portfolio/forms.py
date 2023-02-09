"""Forms for the VC portfolio management site"""
from django import forms
from portfolio.models import individual_create, residentialAddress
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# Form for creating an individual / client
class IndividualCreateForm(forms.ModelForm):
    class Meta:
        model = individual_create
        fields = ["AngelListLink", "CrunchbaseLink", "LinkedInLink", 
                  "Company", "Position", "Email", "PrimaryNumber", "SecondaryNumber"]
        widgets = {
            "PrimaryNumber": PhoneNumberPrefixWidget(initial="UK"),
            "SecondaryNumber": PhoneNumberPrefixWidget(initial="UK")
        }
# Form for creating addresses
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = residentialAddress
        fields = ['address_line1', 'address_line2', 'postal_code', 'city', 'state', 'country']
        exclude = ('individual',)
        widgets = {
            "country": CountrySelectWidget()
        }

