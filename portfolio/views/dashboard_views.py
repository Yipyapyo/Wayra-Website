from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView

from portfolio.forms.company_form import CompanyCreateForm
from portfolio.models import Company, Programme, Investment, InvestorCompany, Portfolio_Company


# Create your views here.
@login_required
def dashboard(request):
    """The main dashboard page of the website."""

    # Data for the each company will be listed here.
    page_number = request.GET.get('page', 1)

    if request.session['company_filter'] == 3:
        investor_companies = InvestorCompany.objects.all()
        companies = Company.objects.filter(id__in=investor_companies.values('company'), is_archived=False).order_by('id')
    elif request.session['company_filter'] == 2:
        companies = Portfolio_Company.objects.filter(is_archived=False).order_by('id')
    else:
        companies = Company.objects.filter(is_archived=False).order_by('id')

    paginator = Paginator(companies, 6)

    try:
        companies_page = paginator.page(page_number)
    except EmptyPage:
        companies_page = []

    context = {
        "companies": companies_page,
        "search_url": reverse('company_search_result'),
        "placeholder": "Search for a Company"
    }

    return render(request, 'company/main_dashboard.html', context)


@login_required
def searchcomp(request):
    if request.method == "GET":
        searched = request.GET['searchresult']

        response = []

        if (searched == ""):
            response = []
        else:
            # search_result = Company.objects.filter(name__contains=searched, is_archived=False).values()[:5]
            if request.session['company_filter'] == 3:
                investor_companies = InvestorCompany.objects.all()
                search_result = Company.objects.filter(id__in=investor_companies.values('company'), is_archived=False, name__contains=searched)[:5]
            elif request.session['company_filter'] == 2:
                search_result = Portfolio_Company.objects.filter(is_archived=False, name__contains=searched)[:5]
            else:
                search_result = Company.objects.filter(name__contains=searched, is_archived=False).values()[:5]
            response.append(("Companies", list(search_result)))

        search_results_table_html = render_to_string('partials/search/search_results_table.html', {
            'search_results': response, 'searched': searched, 'destination_url': 'portfolio_company'})

        return HttpResponse(search_results_table_html)

    elif request.method == "POST":
        page_number = request.POST.get('page', 1)
        searched = request.POST['searchresult']
        if (searched == ""):
            return redirect('dashboard')
        else:
            if request.session['company_filter'] == 3:
                investor_companies = InvestorCompany.objects.all()
                companies = Company.objects.filter(id__in=investor_companies.values('company'), is_archived=False, name__contains=searched).order_by('id')[:5]
            elif request.session['company_filter'] == 2:
                companies = Portfolio_Company.objects.filter(is_archived=False, name__contains=searched).order_by('id')[:5]
            else:
                companies = Company.objects.filter(name__contains=searched, is_archived=False).values().order_by('id')[:5]

        paginator = Paginator(companies, 6)
        try:
            companies_page = paginator.page(page_number)
        except EmptyPage:
            companies_page = []

        return render(request, 'company/main_dashboard.html', {"companies": companies_page, "searched": searched})


@login_required
def portfolio_company(request, company_id):
    """This page displays information about a single portfolio company"""
    company = Company.objects.get(id=company_id)
    programmes = Programme.objects.filter(Q(participants=company) | Q(partners=company))
    return render(request, 'company/portfolio_company_page.html',
                  {'counter': {1, 2, 3},
                   'contract_counter': {1, 2, 3, 4},
                   'company': company,
                   'programmes': programmes
                   })


class CompanyDetailView(LoginRequiredMixin, ListView):
    template_name = 'company/portfolio_company_page.html'
    context_object_name = 'investments'
    paginate_by = 10

    def dispatch(self, request, company_id, *args, **kwargs):
        self.company = Company.objects.get(id=company_id)
        return super().dispatch(request, company_id, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        context['is_investor_company'] = InvestorCompany.objects.filter(company=self.company).exists()
        context['counter'] = [1, 2, 3]
        context['contract_counter'] = [1, 2, 3, 4]
        context['programmes'] = Programme.objects.filter(participants__name=self.company.name)
        return context

    def get_queryset(self):
        self.investments = Investment.objects.filter(investor__company=self.company).order_by('id')
        return self.investments


@login_required
def create_company(request):
    """This page presents a form to create a company"""
    if request.method == "POST":
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CompanyCreateForm()

    return render(request, 'company/company_create.html', {'form': form})


@login_required
def update_company(request, company_id):
    """This page presents a form to update a company"""
    company = Company.objects.get(id=company_id)

    if request.method == "POST":
        form = CompanyCreateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('portfolio_company', company_id=company.id)
    else:
        form = CompanyCreateForm(instance=company)

    return render(request, 'company/company_update.html', {'form': form, 'company_id': company.id})


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
    return redirect('archive_page')

@login_required
def change_company_layout(request, layout_number):
    request.session['company_layout'] = layout_number
    return redirect('dashboard')

@login_required
def change_company_filter(request):
    if request.method == "GET":
        filter_number = request.GET['filter_number']
        page_number = request.GET.get('page', 1)
        if filter_number:
            request.session['company_filter'] = filter_number
        else:
            request.session['company_filter'] = 1

        if request.session['company_filter'] == '3':
            investor_companies = InvestorCompany.objects.all()
            result = Company.objects.filter(id__in=investor_companies.values('company'), is_archived=False).order_by('id')
        elif request.session['company_filter'] == '2':
            result = Portfolio_Company.objects.filter(is_archived=False).order_by('id')
        elif request.session['company_filter'] == '1':
            result = Company.objects.filter(is_archived=False).values().order_by('id')

        paginator = Paginator(result, 6)

        try:
            companies_page = paginator.page(page_number)
        except EmptyPage:
            companies_page = []

        context = {
            "companies": companies_page,
            "search_url": reverse('company_search_result'),
            "placeholder": "Search for a Company",
            "async_company_layout": int(request.session["company_layout"]),
        }

        search_results_table_html = render_to_string('company/company_dashboard_content_reusable.html', context)

        return HttpResponse(search_results_table_html)
    