from django import forms
from portfolio.models.founder_model import Founder
from portfolio.models.company_model import Company

class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        fields = ['company', 'additionalInformation']

        company = forms.ModelMultipleChoiceField(
            label="Select company founded", 
            widget=forms.CheckboxSelectMultiple,  
            queryset=Company.objects.all()
        )