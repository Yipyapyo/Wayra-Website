from django.shortcuts import render
from .forms import IndividualCreateForm, AddressCreateForm
from .models import Individual, ResidentialAddress
from django.shortcuts import redirect, render

# Create your views here.

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
    return render(request, "individual_create.html", context=context)

"""
List of individuals
"""
def individual_page(request):
    data = {'object_list': Individual.objects.all()}
    return render(request, "individual_page.html", data)

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
    return render(request, 'individual_update.html', context=context)

"""
Delete a particular individual
"""
def individual_delete(request, id):
    individualForm = Individual.objects.get(id=id)
    if request.method == 'POST':
        individualForm.delete()
        return redirect('individual_page')
    return render(request, 'individual_delete.html')
