from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm
from portfolio.models import Individual, ResidentialAddress
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage


"""
Create an individual.
"""

def individual_create(request):
    individualForm = IndividualCreateForm()
    addressForms = AddressCreateForm()

    if request.method == "POST":
        individualForm = IndividualCreateForm(request.POST, prefix="form1")
        addressForms = AddressCreateForm(request.POST, prefix="form2")
        # addressForms = [AddressCreateForm(request.POST, prefix=str(x)) for x in range (0, 1)]
        if individualForm.is_valid() and addressForms.is_valid():
            # if individualForm.is_valid() and all([addressForms.is_valid() for af in addressForms]):
            new_individual = individualForm.save()
            new_address = addressForms.save(commit=False)
            new_address.individual = new_individual
            new_address.save()
            return redirect("individual_page")
    else:
        individualForm = IndividualCreateForm(prefix="form1")
        addressForms = AddressCreateForm(prefix="form2")

    context = {
        'individualForm': individualForm,
        'addressForms': addressForms,
    }
    return render(request, "individual/individual_create.html", context=context)


"""
List of individuals
"""

@login_required
def individual_page(request):
    page_number = request.GET.get('page', 1)
    individuals = Individual.objects.filter(is_archived=False).order_by('id')
    paginator = Paginator(individuals, 6)
    try:
        individuals_page = paginator.page(page_number)
    except EmptyPage:
        individuals_page = []

    data = {
        'individuals': individuals_page,
    }

    return render(request, "individual/individual_page.html", data)


"""
Update a particular individual's information
"""

def individual_update(request, id):
    individualForm = Individual.objects.get(id=id)
    addressForms = ResidentialAddress.objects.get(id=id)
    if request.method == 'POST':
        form1 = IndividualCreateForm(request.POST, instance=individualForm, prefix="form1")
        form2 = AddressCreateForm(request.POST, instance=addressForms, prefix="form2")
        if form1.is_valid() and form2.is_valid():
            updated_individual = form1.save()
            updated_address = form2.save(commit=False)
            updated_address.individual = updated_individual
            updated_address.save()
            return redirect("individual_page")
    else:
        form1 = IndividualCreateForm(instance=individualForm, prefix="form1")
        form2 = AddressCreateForm(instance=addressForms, prefix="form2")
    context = {
        'individualForm': form1,
        'addressForms': form2,
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

"""
View an individual profile page
"""

@login_required
def individual_profile(request, id):
    individual = Individual.objects.get(id=id)
    return render(request, 'individual/individual_about_page.html', {"individual": individual})

@login_required
def archive_individual(request, id):
    """Handles the deletion of a company"""
    individual = Individual.objects.get(id=id)
    individual.archive()
    return redirect('individual_profile', id=individual.id)

@login_required
def unarchive_individual(request, id):
    """Handles the deletion of a company"""
    individual = Individual.objects.get(id=id)
    individual.unarchive()
    return redirect('individual_profile', id=individual.id)
