from django.shortcuts import render
from .forms import IndividualCreateForm, AddressCreateForm
from .models import individual_create, residentialAddress
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
    return render(request, "individual_page.html")