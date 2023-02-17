"""Forms for the VC portfolio management site"""
from django import forms
from portfolio.models import Individual, ResidentialAddress
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget


# Form for creating an individual / client
class IndividualCreateForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ["AngelListLink", "CrunchbaseLink", "LinkedInLink",
                  "Company", "Position", "Email", "PrimaryNumber", "SecondaryNumber"]
        # widgets = {
        #     "PrimaryNumber": PhoneNumberPrefixWidget(initial="UK"),
        #     "SecondaryNumber": PhoneNumberPrefixWidget(initial="UK")
        # }

    def __init__(self, *args, **kwargs):
        super(IndividualCreateForm, self).__init__(*args, **kwargs)
        self.fields['PrimaryNumber'].widget = PhoneNumberPrefixWidget()
        self.fields['SecondaryNumber'].widget = PhoneNumberPrefixWidget()


# Form for creating addresses
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = ResidentialAddress
        fields = ['address_line1', 'address_line2', 'postal_code', 'city', 'state', 'country']
        exclude = ('individual',)
        widgets = {
            "country": CountrySelectWidget()
        }