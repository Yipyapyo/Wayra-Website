from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from portfolio.forms import AddressCreateForm, PastExperienceForm
from portfolio.forms.investor_individual_form import InvestorIndividualForm
from portfolio.models import ResidentialAddress
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.models.past_experience_model import PastExperience

"""
Create a investor_individual.
"""


@login_required
def investor_individual_create(request):
    if request.method == "POST":
        address_forms = AddressCreateForm(request.POST, prefix="form2")
        past_experience_forms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0, 2)]
        investor_individual_form = InvestorIndividualForm(request.POST, prefix="form1")
        if investor_individual_form.is_valid() and address_forms.is_valid() and all(
                [pf.is_valid() for pf in past_experience_forms]):
            investor_individual = investor_individual_form.save()
            new_address = address_forms.save(commit=False)
            new_address.individual = investor_individual
            new_address.save()
            for pf in past_experience_forms:
                new_past_experience = pf.save(commit=False)
                new_past_experience.individual = investor_individual
                new_past_experience.duration = new_past_experience.end_year - new_past_experience.start_year
                new_past_experience.save()
            return redirect("individual_page")
    else:
        investor_individual_form = InvestorIndividualForm(prefix="form1")
        address_forms = AddressCreateForm(prefix="form2")
        past_experience_forms = [PastExperienceForm(prefix=str(x)) for x in range(0, 2)]

    context = {
        'addressForms': address_forms,
        'pastExperienceForms': past_experience_forms,
        'investorIndividualForm': investor_individual_form
    }
    return render(request, "individual/investor_individual_create.html", context=context)


"""
Delete a investor_individual.
"""


@login_required
def investor_individual_delete(request, id):
    investor_individual_instance = InvestorIndividual.objects.get(id=id)
    if request.method == 'POST':
        investor_individual_instance.delete()
        return redirect('individual_page')
    return render(request, 'individual/investor_individual_delete.html')


"""
Modify a investor_individual.
"""


@login_required
def investor_individual_modify(request, id):
    investor_individual_form = InvestorIndividual.objects.get(id=id)
    address_forms = ResidentialAddress.objects.get(id=id)
    past_experience_list = PastExperience.objects.filter(individual=investor_individual_form)
    if request.method == 'POST':
        form1 = InvestorIndividualForm(request.POST, instance=investor_individual_form, prefix="form1")
        form2 = AddressCreateForm(request.POST, instance=address_forms, prefix="form2")
        forms3 = [PastExperienceForm(request.POST, instance=p, prefix="past_experience_{}".format(p.id)) for p in
                  past_experience_list]
        if form1.is_valid() and form2.is_valid() and all([pf.is_valid() for pf in forms3]):
            updated_investor_individual = form1.save()
            updated_address = form2.save(commit=False)
            updated_address.individual = updated_investor_individual
            updated_address.save()
            for pf in forms3:
                updated_experience = pf.save(commit=False)
                updated_experience.individual = updated_investor_individual
                updated_experience.duration = updated_experience.end_year - updated_experience.start_year
                updated_experience.save()
            return redirect("individual_page")
    else:
        form1 = InvestorIndividualForm(instance=investor_individual_form, prefix="form1")
        form2 = AddressCreateForm(instance=address_forms, prefix="form2")
        forms3 = [PastExperienceForm(instance=p, prefix="past_experience_{}".format(p.id)) for p in
                  past_experience_list]
    context = {
        'investorIndividualForm': form1,
        'addressForms': form2,
        'pastExperienceForms': forms3,
    }
    return render(request, 'individual/investor_individual_modify.html', context=context)
