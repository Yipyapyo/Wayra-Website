from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json 
from django.core.paginator import Paginator, EmptyPage
from django.urls import reverse


# Create your views here.
@login_required
def dashboard(request):
    '''The main dashboard page of the website.'''

    # Data for the each company will be listed here.
    page_number = request.GET.get('page', 1)

    companies = Company.objects.filter(is_archived=False).order_by('id')

    paginator = Paginator(companies, 6)

    try:
        companies_page = paginator.page(page_number)
    except EmptyPage:
        companies_page = []

    context = {
        "companies": companies_page,
        "search_url": reverse('search_result'),
        "placeholder":"Search for a Company"
    }

    return render(request, 'company/main_dashboard.html', context)

@login_required
def searchcomp(request):

    if request.method == "GET":

        searched = request.GET['searchresult']
        
        response = []

        if(searched == ""):
            response = []
        else:
            search_result = Company.objects.filter(name__contains=searched).values()
            response.append(("Companies",list(search_result)))
        

        search_results_table_html = render_to_string('partials/search/search_results_table.html', {
        'search_results': response, 'searched':searched, 'destination_url':'portfolio_company'})

        return HttpResponse(search_results_table_html)

    elif request.method == "POST":
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']
        if(searched == ""):
            return redirect('dashboard')
        else:
            companies = Company.objects.filter(name__contains=searched).values()
        
        paginator = Paginator(companies, 6)
        try:
            companies_page = paginator.page(page_number)
        except EmptyPage:
            companies_page = []

        return render(request, 'company/main_dashboard.html', {"companies": companies_page, "searched":searched})

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

@login_required
def update_company(request, company_id):
    '''This page presents a form to update a company'''
    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = CompanyCreateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('portfolio_company', company_id=company.id)
    else:
        form = CompanyCreateForm(instance=company)

    return render(request, 'company/company_update.html', {'form':form, 'company_id':company.id})

@login_required
def delete_company(request, company_id):
    """Handles the deletion of a company"""
    company = Company.objects.get(id=company_id)

    try:
        company.delete()
    except Company.DoesNotExist:
        pass
    return redirect('dashboard')

@login_required
def archive_company(request, company_id):
    """Handles the deletion of a company"""
    company = Company.objects.get(id=company_id)
    company.archive()
    return redirect('portfolio_company', company_id=company.id)

@login_required
def unarchive_company(request, company_id):
    """Handles the deletion of a company"""
    company = Company.objects.get(id=company_id)
    company.unarchive()
    return redirect('portfolio_company', company_id=company.id)