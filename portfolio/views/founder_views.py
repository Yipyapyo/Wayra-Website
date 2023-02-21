from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress
from portfolio.models.past_experience_model import pastExperience
from portfolio.models.founder_model import Founder
from portfolio.forms.founder_form import FounderForm
from django.shortcuts import redirect, render

"""
Create a founder.
"""

def founder_create(request):
    if request.method == "POST":
        addressForms = AddressCreateForm(request.POST, prefix="form2")
        pastExperienceForms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0,2)]
        founder_form = FounderForm(request.POST, prefix="form1")
        if founder_form.is_valid() and addressForms.is_valid() and all([pf.is_valid() for pf in pastExperienceForms]):
            founder = founder_form.save()     
            new_address = addressForms.save(commit=False)
            new_address.individual = founder
            new_address.save()
            for pf in pastExperienceForms:
                new_pastExperience = pf.save(commit=False)
                new_pastExperience.individual = founder
                new_pastExperience.duration = new_pastExperience.end_year - new_pastExperience.start_year
                new_pastExperience.save()  
            return redirect("individual_page")
    else:
        founder_form = FounderForm(prefix="form1")
        addressForms = AddressCreateForm(prefix="form2")
        pastExperienceForms = [PastExperienceForm(prefix=str(x)) for x in range(0,2)]

    context = {
        'addressForms': addressForms,
        'pastExperienceForms': pastExperienceForms,
        'founderForm': founder_form
    }
    return render(request, "individual/founder_create.html", context=context)

"""
Delete a founder.
"""

def founder_delete(request):
    founderInstance = Founder.objects.get(id=id)
    if request.method == 'POST':
        founderInstance.delete()
        return redirect('individual_page')
    return render(request, 'individual/founder_delete.html')