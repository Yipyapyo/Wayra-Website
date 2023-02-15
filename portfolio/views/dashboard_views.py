from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import logging


# Create your views here.
@login_required
def dashboard(request):
    '''The main dashboard page of the website.'''

    # Data for the each company will be listed here.

    # An array of dictonaries will be created
    # Until the Add company functionality is developed, we will have a set dataset.

    companies = [

        {'Company': "Wayra", 'Founders': "John Doe", 'Year_operation': "12 years", "Investors": "Wayra UK Limited"},
        {'Company': "Apple", 'Founders': "Steve Jobs", 'Year_operation': "30 years", "Investors": "Saadh Ltd"},
        {'Company': "Microsoft", 'Founders': "Bill Gates", 'Year_operation': "30 years",
         "Investors": "Wayra UK Limited"},
        {'Company': "Nation of Pakistan", 'Founders': "Saadh", 'Year_operation': "1 years", "Investors": "Me"},
        {'Company': "Nation of India", 'Founders': "Not Saadh", 'Year_operation': "2 years", "Investors": "Not me"}

    ]

    return render(request, 'main_dashboard.html', {"companies": companies, })

@login_required
def searchcomp(request):
    # Data for the each company will be listed here.

    # An array of dictonaries will be created
    # Until the Add company functionality is developed, we will have a set dataset.

    companies = [

        {'Company': "Wayra", 'Founders': "John Doe", 'Year_operation': "12 years", "Investors": "Wayra UK Limited"},
        {'Company': "Apple", 'Founders': "Steve Jobs", 'Year_operation': "30 years", "Investors": "Saadh Ltd"},
        {'Company': "Microsoft", 'Founders': "Bill Gates", 'Year_operation': "30 years",
         "Investors": "Wayra UK Limited"},
        {'Company': "Nation of Pakistan", 'Founders': "Saadh", 'Year_operation': "1 years", "Investors": "Me"},
        {'Company': "Nation of India", 'Founders': "Not Saadh", 'Year_operation': "2 years", "Investors": "Not me"},
        {'Company': "ApplePotato", 'Founders': "Steve Zahid", 'Year_operation': "32 years", "Investors": "Benq Ltd"}

    ]

    searched_companies = []

    if request.method == "POST":

        # ADD CLEANING

        searched = request.POST['searchresult']

        logging.debug(searched)

        for comp in companies:

            if searched in comp["Company"]:
                searched_companies.append(comp)

        return render(request, 'main_dashboard.html', {"companies": searched_companies})


    else:
        return render(request, 'main_dashboard.html')

@login_required
def portfolio_company(request):
    '''This page displays information about a single portfolio company'''
    return render(request, 'portfolio_company_page.html', {'counter': {1, 2, 3}, 'contract_counter': {1, 2, 3, 4}})

@login_required
def create_company(request):
    '''This page presents a form to create a company'''
    return render(request, 'company_create.html')