from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json 


# Create your views here.
@login_required
def dashboard(request):
    '''The main dashboard page of the website.'''

    # Data for the each company will be listed here.

    companies = Company.objects.all()

    return render(request, 'company/main_dashboard.html', {"companies": companies})

@login_required
def searchcomp(request):

    if request.method == "GET":

        searched = request.GET['searchresult']
        print(f"searched: {searched}")

        if(searched == ""):
            search_result = {}
        else:
            search_result = Company.objects.filter(name__contains=searched).values()
        
        search_results_table_html = render_to_string('partials/utilities/search_results_table.html', {
        'search_results': list(search_result),
    })

        # Return the resulting HTML as an HTTP response
        return HttpResponse(search_results_table_html)
        # return HttpResponse(list(search_result))


    else:
        return HttpResponse("Request method is not a GET")

@login_required
def portfolio_company(request, company_id):
    '''This page displays information about a single portfolio company'''
    company = Company.objects.get(id=company_id)

    return render(request, 'company/portfolio_company_page.html', {'counter': {1, 2, 3}, 'contract_counter': {1, 2, 3, 4}, 'company':company})

@login_required
def create_company(request):
    '''This page presents a form to create a company'''
    if request.method == "POST":
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CompanyCreateForm()

    return render(request, 'company/company_create.html', {'form':form})