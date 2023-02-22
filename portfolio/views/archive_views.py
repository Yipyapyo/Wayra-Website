from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from portfolio.models import Company, Individual
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage

"""Archive views"""
@login_required
def archive(request):
    '''This ius the archive page. ONLY VIEWED BY ADMINS'''
    page_number = request.GET.get('page', 1)

    companies = Company.objects.all()

    paginator = Paginator(companies, 5)

    try:
        companies_page = paginator.page(page_number)
    except EmptyPage:
        companies_page = []

    context = {
        "companies":companies_page,
        "search_url": reverse('archive_search'),
        "placeholder":"Search through the archive"
    }

    return render(request, 'archive/archive_page.html', context)

@login_required
def archive_search(request):

    if request.method == "GET":

        searched = request.GET['searchresult']

        response = []

        if(searched == ""):
            response = []
        else:
            company_search_result = Company.objects.filter(name__contains=searched).values()
            individual_search_result = Individual.objects.filter(name__contains=searched).values()
            response.append(("Companies",list(company_search_result)))
            response.append(("Individuals",list(individual_search_result)))
        
        search_results_table_html = render_to_string('partials/search/search_results_table.html', {
        'search_results': response, 'searched':searched, 'destination_url':'portfolio_company'})
 
        return HttpResponse(search_results_table_html)

    else:
        return HttpResponse("Request method is not a GET")
