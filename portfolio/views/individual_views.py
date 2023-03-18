from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.models import Individual, ResidentialAddress, InvestorIndividual, Founder
from portfolio.models.investment_model import Investor
from portfolio.models.past_experience_model import PastExperience
from portfolio.forms.founder_form import FounderForm
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse



"""
Create an individual.
"""


def individual_search(request):
    if request.method == "GET":
        searched = request.GET['searchresult']
        
        response = []

        if(searched == ""):
            response = []
        else:
            search_result = Individual.objects.filter(name__contains=searched).values()[:5]
            response.append(("Individual", list(search_result),{'destination_url':'individual_profile'}))
        

        individual_search_results_table_html = render_to_string('partials/search/search_results_table.html', {
        'search_results': response, 'searched':searched, "destination_url":"individual_profile"})

        return HttpResponse(individual_search_results_table_html)


    elif request.method == "POST":
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']

        if searched == "":
            return redirect('individual_page')
        else:
            individuals = Individual.objects.filter(name__contains=searched).values()
            paginator = Paginator(individuals, 6)

        try:
            individual_page = paginator.page(page_number)
        except EmptyPage:
            individual_page = []

        return render(request, 'individual/individual_page.html', {"individuals": individual_page, "searched":searched})

    else:
        return HttpResponse("Request method is not a GET")




@login_required
def individual_create(request):

    if request.method == "POST":
        individual_form = IndividualCreateForm(request.POST, prefix="form1")
        address_forms = AddressCreateForm(request.POST, prefix="form2")
        past_experience_forms = [PastExperienceForm(request.POST, prefix=str(x)) for x in range(0,2)]      
        if individual_form.is_valid() and address_forms.is_valid() and all([pf.is_valid() for pf in past_experience_forms]):
            new_individual = individual_form.save()
            new_address = address_forms.save(commit=False)
            new_address.individual = new_individual
            new_address.save()
            for pf in past_experience_forms:
                new_past_experience = pf.save(commit=False)
                new_past_experience.individual = new_individual
                new_past_experience.duration = new_past_experience.end_year - new_past_experience.start_year
                new_past_experience.save()
            return redirect("individual_page")
    else:
        individual_form = IndividualCreateForm(prefix="form1")
        address_forms = AddressCreateForm(prefix="form2")
        past_experience_forms = [PastExperienceForm(prefix=str(x)) for x in range(0,2)]

    context = {
        'individualForm': individual_form,
        'addressForms': address_forms,
        'pastExperienceForms': past_experience_forms,
    }
    return render(request, "individual/individual_create.html", context=context)


"""
List of individuals
"""

@login_required
def individual_page(request):
    page_number = request.GET.get('page', 1)
    # individuals = Individual.objects.filter(is_archived=False).order_by('id')

    if request.session['individual_filter'] == '2':
        founder_individuals = Founder.objects.all()
        individuals = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), is_archived=False).order_by('id')
    elif request.session['individual_filter'] == '3':
        investors = Investor.objects.all()
        individuals = Individual.objects.filter(id__in=investors.values('individual'), is_archived=False).order_by('id')
    else:
        individuals = Individual.objects.filter(is_archived=False).values().order_by('id')

    cast_individuals = list()
    for individual in individuals:
        cast_individuals.append(individual.as_child_class)

    paginator = Paginator(cast_individuals, 6)

    try:
        individuals_page = paginator.page(page_number)
    except EmptyPage:
        individuals_page = []

    data = {
        'individuals': individuals_page,
        "search_url": reverse('individual_search_result'),
        "placeholder": "Search for an Individual"
    }



    return render(request, "individual/individual_page.html", data)


"""
Update a particular individual's information
"""
@login_required
def individual_update(request, id):
    individual_form = Individual.objects.get(id=id)
    address_forms = ResidentialAddress.objects.get(id=id)
    past_experience_list = PastExperience.objects.filter(individual=individual_form)
    past_experience_forms = [PastExperienceForm(instance=p, prefix="past_experience") for p in past_experience_list]
    if request.method == 'POST':
        form1 = IndividualCreateForm(request.POST, instance=individual_form, prefix="form1")
        form2 = AddressCreateForm(request.POST, instance=address_forms, prefix="form2")
        forms3 = [PastExperienceForm(request.POST, instance=p, prefix="past_experience") for p in past_experience_list]
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
        form1 = IndividualCreateForm(instance=individual_form, prefix="form1")
        form2 = AddressCreateForm(instance=address_forms, prefix="form2")
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
@login_required
def individual_delete(request, id):
    individual_form = Individual.objects.get(id=id)
    if request.method == 'POST':
        individual_form.delete()
        return redirect('individual_page')
    return render(request, 'individual/individual_delete.html')

"""
View an individual profile page
"""

@login_required
def individual_profile(request, id):
    individual = Individual.objects.get(id=id)
    if(not individual.is_archived or (individual.is_archived and request.user.is_staff)):
        return render(request, 'individual/individual_about_page.html', {"individual": individual})
    else: 
        return redirect('individual_page')

"""
Archive an Individual
"""

@login_required
def archive_individual(request, id):
    """Handles the deletion of a company"""
    individual = Individual.objects.get(id=id)
    individual.archive()
    return redirect('individual_profile', id=individual.id)

"""
Unarchive an Individual
"""

@login_required
def unarchive_individual(request, id):
    """Handles the deletion of a company"""
    individual = Individual.objects.get(id=id)
    individual.unarchive()
    return redirect('individual_profile', id=individual.id)

"""
Asynchronously filter individuals on the individuals page
"""

@login_required
def change_individual_filter(request):
    if request.method == "GET":
        filter_number = request.GET['filter_number']
        page_number = request.GET.get('page', 1)
        if filter_number:
            request.session['individual_filter'] = filter_number
        else:
            request.session['individual_filter'] = 1

        if request.session['individual_filter'] == '2':
            founder_individuals = Founder.objects.all()
            result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), is_archived=False).order_by('id')
        elif request.session['individual_filter'] == '3':
            investors = Investor.objects.all()
            result = Individual.objects.filter(id__in=investors.values('individual'), is_archived=False).order_by('id')
        else:
            result = Individual.objects.filter(is_archived=False).values().order_by('id')

        paginator = Paginator(result, 6)

        try:
            individual_page = paginator.page(page_number)
        except EmptyPage:
            individual_page = []

        context = {
            "individuals": individual_page,
            "search_url": reverse('individual_search_result'),
            "placeholder": "Search for a Individual",
            "async_individual_layout": int(request.session["individual_layout"]),
        }

        search_results_table_html = render_to_string('individual/individual_page_content_reusable.html', context)

        return HttpResponse(search_results_table_html)

@login_required
def change_individual_layout(request):
    if request.method == "GET":
        layout_number = request.GET['layout_number']
        page_number = request.GET.get('page', 1)
        if layout_number:
            request.session['individual_layout'] = layout_number
        else:
            request.session['individual_layout'] = 1

        if request.session['individual_filter'] == '2':
            founder_individuals = Founder.objects.all()
            result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), is_archived=False).order_by('id')
        elif request.session['individual_filter'] == '3':
            investors = Investor.objects.all()
            result = Individual.objects.filter(id__in=investors.values('individual'), is_archived=False).order_by('id')
        else:
            result = Individual.objects.filter(is_archived=False).values().order_by('id')

        paginator = Paginator(result, 6)

        try:
            individuals_page = paginator.page(page_number)
        except EmptyPage:
            individuals_page = []

        context = {
            "individuals": individuals_page,
            "search_url": reverse('individual_search_result'),
            "placeholder": "Search for a Individual",
            "async_individual_layout": int(request.session["individual_layout"]),
        }

        search_results_table_html = render_to_string('individual/individual_page_content_reusable.html', context)

        return HttpResponse(search_results_table_html)