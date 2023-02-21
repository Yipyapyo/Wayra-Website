from django import forms
from portfolio.models.founder_model import Founder
from portfolio.models.individual_model import Individual

class FounderForm(forms.ModelForm):
    companyFounded = forms.CharField(label='Company Founded', max_length=100, initial="USA")
    additionalInformation = forms.CharField(label='Additional Information', max_length=500, required=False)

    class Meta:
        model = Founder
        fields = ['AngelListLink', 'CrunchbaseLink', 'LinkedInLink',
                  'Company', 'Position', 'Email', 'PrimaryNumber', 'SecondaryNumber', 'companyFounded', 'additionalInformation']
        exclude = ('isFounder',)

        # company = forms.ModelMultipleChoiceField(
        #     label="Select company founded", 
        #     widget=forms.CheckboxSelectMultiple,  
        #     queryset=Company.objects.all()
        # )