from django.shortcuts import render
from .forms import IndividualCreateForm, AddressCreateForm
from .models import individual_create, residentialAddress
from django.shortcuts import redirect, render

# Create your views here.

"""
Create an individual.
"""
def individual_create(request):
    if request.method == "POST":
        individualForm = IndividualCreateForm(request.POST)
        addressForms = [AddressCreateForm(request.POST, prefix=str(x)) for x in range (0, 1)]
        if individualForm.is_valid() and all([addressForms.is_valid() for af in addressForms]):
            new_individual = individualForm.save()
            for af in addressForms:
                new_address = af.save(commit=False)
                new_address.individual = new_individual
                new_address.save()
                return redirect("individual_page")
    return render(request, "individual_create.html")

"""
List of individuals
"""
def individual_page(request):
    return render(request, "individual_page.html")