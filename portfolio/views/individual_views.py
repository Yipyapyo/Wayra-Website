from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress
from portfolio.models.past_experience_model import pastExperience
from portfolio.forms.founder_form import FounderForm
from django.shortcuts import redirect, render


"""
Create an individual.
"""

def individual_create(request):

    if request.method == "POST":
        individualForm = IndividualCreateForm(request.POST, prefix="form1")
        addressForms = AddressCreateForm(request.POST, prefix="form2")
        pastExperienceForms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0,2)]
        founder_form = FounderForm(request.POST)        
        if individualForm.is_valid() and addressForms.is_valid() and all([pf.is_valid() for pf in pastExperienceForms]) and founder_form.is_valid():
            new_individual = individualForm.save(commit=False)
            if founder_form.cleaned_data['companyFounded'] is not None:
                founder = founder_form.save(commit=False)
                founder.individual = new_individual
                new_individual.isFounder = True
                new_individual.founder = founder
                new_individual.save()
                founder.save()
                new_address = addressForms.save(commit=False)
                new_address.individual = new_individual
                new_address.save()
                for pf in pastExperienceForms:
                    new_pastExperience = pf.save(commit=False)
                    new_pastExperience.individual = new_individual
                    new_pastExperience.duration = new_pastExperience.end_year - new_pastExperience.start_year
                    new_pastExperience.save()
            else:
                new_individual.isFounder = False
                new_individual.save()
                new_address = addressForms.save(commit=False)
                new_address.individual = new_individual
                new_address.save()
                for pf in pastExperienceForms:
                    new_pastExperience = pf.save(commit=False)
                    new_pastExperience.individual = new_individual
                    new_pastExperience.duration = new_pastExperience.end_year - new_pastExperience.start_year
                    new_pastExperience.save()
            return redirect("individual_page")
    else:
        individualForm = IndividualCreateForm(prefix="form1")
        founder_form = FounderForm()
        addressForms = AddressCreateForm(prefix="form2")
        pastExperienceForms = [PastExperienceForm(prefix=str(x)) for x in range(0,2)]

    context = {
        'individualForm': individualForm,
        'addressForms': addressForms,
        'pastExperienceForms': pastExperienceForms,
        'founderForm': founder_form
    }
    return render(request, "individual/individual_create.html", context=context)


"""
List of individuals
"""


def individual_page(request):
    data = {'object_list': Individual.objects.all()}
    return render(request, "individual/individual_page.html", data)


"""
Update a particular individual's information
"""


def individual_update(request, id):
    individualForm = Individual.objects.get(id=id)
    founderForm = individualForm.founder
    addressForms = ResidentialAddress.objects.get(id=id)
    past_experience_list = pastExperience.objects.filter(individual=individualForm)
    past_experience_forms = [PastExperienceForm(instance=p, prefix="past_experience") for p in past_experience_list]
    if request.method == 'POST':
        form1 = IndividualCreateForm(request.POST, instance=individualForm, prefix="form1") 
        form4 = FounderForm(request.POST, instance=founderForm, prefix="form4")
        form2 = AddressCreateForm(request.POST, instance=addressForms, prefix="form2")
        forms3 = [PastExperienceForm(request.POST, instance=p, prefix="past_experience") for p in past_experience_list]
        if form1.is_valid() and form2.is_valid() and all([pf.is_valid() for pf in forms3]) and form4.is_valid():
            updated_founder = form4.save(commit=False)
            updated_individual = form1.save(commit=False)
            updated_individual.founder = updated_founder
            updated_founder.individual = updated_individual
            updated_individual.save()
            updated_founder.save()
            # updated_founder.save()
            updated_address = form2.save(commit=False)
            updated_address.individual = updated_individual
            updated_address.save()
            for pf in forms3:
                updated_experience = pf.save(commit=False)
                updated_experience.individual = updated_individual
                updated_experience.duration = updated_experience.end_year - updated_experience.start_year
                updated_experience.save()
            return redirect("individual_page")
    else:
        if individualForm.isFounder:
            form1 = FounderForm(instance=individualForm.founder, prefix="form1")
        else:
            form1 = IndividualCreateForm(instance=individualForm, prefix="form1")
            form2 = AddressCreateForm(instance=addressForms, prefix="form2")
            forms3 = past_experience_forms
            form4 = IndividualCreateForm(instance=individualForm, prefix="form4")
    context = {
        'individualForm': form4,
        'addressForms': form2,
        'pastExperienceForms': forms3,
    }
    return render(request, 'individual/individual_update.html', context=context)


"""
Delete a particular individual
"""


def individual_delete(request, id):
    individualForm = Individual.objects.get(id=id)
    if request.method == 'POST':
        individualForm.delete()
        return redirect('individual_page')
    return render(request, 'individual/individual_delete.html')
