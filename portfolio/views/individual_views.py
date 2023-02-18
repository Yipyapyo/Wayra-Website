from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress
from portfolio.models.past_experience_model import pastExperience
from django.shortcuts import redirect, render


"""
Create an individual.
"""


def individual_create(request):

    if request.method == "POST":
        individualForm = IndividualCreateForm(request.POST, prefix="form1")
        addressForms = AddressCreateForm(request.POST, prefix="form2")
        pastExperienceForms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0,2)]        
        if individualForm.is_valid() and addressForms.is_valid() and all([pf.is_valid() for pf in pastExperienceForms]):
            new_individual = individualForm.save()
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
        addressForms = AddressCreateForm(prefix="form2")
        pastExperienceForms = [PastExperienceForm(prefix=str(x)) for x in range(0,2)]

    context = {
        'individualForm': individualForm,
        'addressForms': addressForms,
        'pastExperienceForms': pastExperienceForms
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
    addressForms = ResidentialAddress.objects.get(id=id)
    past_experience_list = pastExperience.objects.filter(individual=individualForm)
    past_experience_forms = [PastExperienceForm(instance=p, prefix="past_experience") for p in past_experience_list]
    if request.method == 'POST':
        form1 = IndividualCreateForm(request.POST, instance=individualForm, prefix="form1")
        form2 = AddressCreateForm(request.POST, instance=addressForms, prefix="form2")
        forms3 = [PastExperienceForm(request.POST, instance=p, prefix="past_experience") for p in past_experience_list]
        # formLists = [];
        # for ef in pastExperienceForms:
        #     formLists.append(PastExperienceForm(request.POST, instance=ef))
        if form1.is_valid() and form2.is_valid() and all([pf.is_valid() for pf in forms3]):
            updated_individual = form1.save()
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
        form1 = IndividualCreateForm(instance=individualForm, prefix="form1")
        form2 = AddressCreateForm(instance=addressForms, prefix="form2")
        forms3 = past_experience_forms
    context = {
        'individualForm': form1,
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
