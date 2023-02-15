# from django import forms
# from portfolio.models import Company, Individual


# class CreateProgrammeForm(forms.ModelForm):
#     class Meta:
#         #model = Programme
#         fields = ["name", "cohort"]
#         widgets = {
#             'cohort': forms.NumberInput(attrs = {'min': 1})
#         }
    
#     #Populating partner choices    
#     partners_list = Company.objects.all()
#     PARTNER_CHOICES = []
#     for partner in partners_list:
#         PARTNER_CHOICES.append(partner)
#     partners = forms.MultipleChoiceField(label="Partners", choices = PARTNER_CHOICES, required = True)
    
#     #Populating portfolio company choices
#     #participant_list = Portfolio_Company.objects.all()
#     PARTICIPANT_CHOICES = []
#     # for parti in participant_list:
#     #     PARTICIPANT_CHOICES.append(parti)
#     participants = forms.MultipleChoiceField(label="Participants", choices = PARTICIPANT_CHOICES, required = True)
    
#     #Populating coaches and mentors
#     coaches_list = Individual.objects.all()
#     COACHES_CHOICES = []
#     for coach in coaches_list:
#         COACHES_CHOICES.append(coach)
#     coaches_mentors = forms.MultipleChoiceField(label="Coaches and Mentors", choices = COACHES_CHOICES, required = True)
    
#     def save(self):
#         super().save(commit = False)
#         # #Programme.objects.create(
#         #     name = self.cleaned_data.get("name"),
#         #     cohort = self.cleaned_data.get("cohort"),
            
#         # )