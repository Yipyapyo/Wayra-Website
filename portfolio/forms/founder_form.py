from django import forms
from portfolio.models.founder_model import Founder
from portfolio.models.individual_model import Individual
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FounderForm, self).__init__(*args, **kwargs)
        self.fields['PrimaryNumber'].widget = PhoneNumberPrefixWidget()
        self.fields['SecondaryNumber'].widget = PhoneNumberPrefixWidget()
    