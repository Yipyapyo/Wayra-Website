from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company, Programme
import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
import json
from django.core.paginator import Paginator, EmptyPage


# Create your views here.
@login_required
def dashboard(request):
    '''The main dashboard page of the website.'''

    # Data for the each company will be listed here.
    page_number = request.GET.get('page', 1)

    companies = Company.objects.all()

    paginator = Paginator(companies, 6)

    try:
        companies_page = paginator.page(page_number)
    except EmptyPage:
        companies_page = []

    context = {
        "companies": companies_page,
    }

    return render(request, 'company/main_dashboard.html', context)


@login_required
def searchcomp(request):
    if request.method == "GET":

        searched = request.GET['searchresult']

        if (searched == ""):
            search_result = {}
        else:
            search_result = Company.objects.filter(name__contains=searched).values()

        search_results_table_html = render_to_string('partials/search/search_results_table.html', {
            'search_results': list(search_result), 'searched': searched})

        return HttpResponse(search_results_table_html)

    elif request.method == "POST":
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']
        if (searched == ""):
            return redirect('dashboard')
        else:
            companies = Company.objects.filter(name__contains=searched).values()

        paginator = Paginator(companies, 6)
        try:
            companies_page = paginator.page(page_number)
        except EmptyPage:
            companies_page = []

        return render(request, 'company/main_dashboard.html', {"companies": companies_page, "searched": searched})

    else:
        return HttpResponse("Request method is not a GET")


@login_required
def portfolio_company(request, company_id):
    '''This page displays information about a single portfolio company'''
    company = Company.objects.get(id=company_id)
    programmes = Programme.objects.filter(Q(participants=company) | Q(partners=company))
    return render(request, 'company/portfolio_company_page.html',
                  {'counter': {1, 2, 3},
                   'contract_counter': {1, 2, 3, 4},
                   'company': company,
                   'programmes': programmes
                   })


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

    return render(request, 'company/company_create.html', {'form': form})
