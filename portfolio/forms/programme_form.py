from django import forms
from portfolio.models import Company, Individual, Portfolio_Company, Programme

class MultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class CreateProgrammeForm(forms.ModelForm):
    class Meta:
        #model = Programme
        fields = ["name", "cohort"]
        widgets = {
            'cohort': forms.NumberInput(attrs = {'min': 1})
        }
    
    partners = MultipleChoiceField(
        queryset = Company.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )
    
    participants = MultipleChoiceField(
        queryset = Portfolio_Company.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )
    
    coaches_mentors = MultipleChoiceField(
        queryset = Individual.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )
    
    def save(self):
        super().save(commit = False)
        new_programme = Programme.objects.create(
                            name = self.cleaned_data.get("name"),
                            cohort = self.cleaned_data.get("cohort"),
                        )
        for partner in self.cleaned_data.get("partner"):
            new_programme.partners.add(partner)
        for parti in self.cleaned_data.get("participants"):
            new_programme.participants.get(parti)
        for coach in self.cleaned_data.get("coaches_mentors"):
            new_programme.coaches_mentors.add(coach)
            
    
    #SAVE THE BELOW FOR NOW IN CASE THIS DOESN'T WORK
    
    # #Populating partner choices    
    # partners_list = Company.objects.all()
    # PARTNER_CHOICES = []
    # for partner in partners_list:
    #     PARTNER_CHOICES.append((partner, partner.name))
    # partners = forms.MultipleChoiceField(label="Partners", choices = PARTNER_CHOICES, required = True)
    
    # #Populating portfolio company choices
    # participant_list = Portfolio_Company.objects.all()
    # PARTICIPANT_CHOICES = []
    # for parti in participant_list:
    #     PARTICIPANT_CHOICES.append((parti, parti.name))
    # participants = forms.MultipleChoiceField(label="Participants", choices = PARTICIPANT_CHOICES, required = True)
    
    # #Populating coaches and mentors
    # coaches_list = Individual.objects.all()
    # COACHES_CHOICES = []
    # for coach in coaches_list:
    #     COACHES_CHOICES.append((coach, coach.name))
    # coaches_mentors = forms.MultipleChoiceField(label="Coaches and Mentors", choices = COACHES_CHOICES, required = True)
    
    