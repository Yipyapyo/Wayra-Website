from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress
from portfolio.models.past_experience_model import PastExperience
from portfolio.models.founder_model import Founder
from portfolio.forms.founder_form import FounderForm
from django.shortcuts import redirect, render

"""
Create a founder.
"""


def founder_create(request):
    if request.method == 'POST':
        # address_forms = AddressCreateForm(request.POST, prefix="form2")
        # past_experience_forms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0,2)]
        founder_form = FounderForm(request.POST, prefix="form1")
        # if founder_form.is_valid() and address_forms.is_valid() and all([pf.is_valid() for pf in past_experience_forms]):
        # if founder_form.is_valid() and address_forms.is_valid():
        if founder_form.is_valid():
            print("hi")
            founder_form.save()     
            # new_address = address_forms.save(commit=False)
            # new_address.individual = founder
            # new_address.save()
            # for pf in past_experience_forms:
            #     new_past_experience = pf.save(commit=False)
            #     new_past_experience.individual = founder
            #     new_past_experience.duration = new_past_experience.end_year - new_past_experience.start_year
            #     new_past_experience.save()
            return redirect("individual_page")
    else:
        founder_form = FounderForm(prefix="form1")
        # address_forms = AddressCreateForm(prefix="form2")
        # past_experience_forms = [PastExperienceForm(prefix=str(x)) for x in range(0,2)]

    context = {
        # 'addressForms': address_forms,
        # 'pastExperienceForms': past_experience_forms,
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


"""
Modify a founder.
"""

def founder_modify(request, id):
    founder_form = Founder.objects.get(id=id)
    address_forms = ResidentialAddress.objects.get(id=id)
    past_experience_list = PastExperience.objects.filter(individual=founder_form)
    if request.method == 'POST':
        form1 = FounderForm(request.POST, instance=founder_form, prefix="form1")
        form2 = AddressCreateForm(request.POST, instance=address_forms, prefix="form2")
        forms3 = [PastExperienceForm(request.POST, instance=p, prefix="past_experience_{}".format(p.id)) for p in past_experience_list]
        if form1.is_valid() and form2.is_valid() and all([pf.is_valid() for pf in forms3]):
            updated_founder = form1.save()
            updated_address = form2.save(commit=False)
            updated_address.individual = updated_founder
            updated_address.save()
            for pf in forms3:
                updated_experience = pf.save(commit=False)
                updated_experience.individual = updated_founder
                updated_experience.duration = updated_experience.end_year - updated_experience.start_year
                updated_experience.save()
            return redirect("individual_page")
    else:
        form1 = FounderForm(instance=founder_form, prefix="form1")
        form2 = AddressCreateForm(instance=address_forms, prefix="form2")
        forms3 = [PastExperienceForm(instance=p, prefix="past_experience_{}".format(p.id)) for p in past_experience_list]
    context = {
        'founderForm': form1,
        'addressForms': form2,
        'pastExperienceForms': forms3,
    }
    return render(request, 'individual/founder_modify.html', context=context)
