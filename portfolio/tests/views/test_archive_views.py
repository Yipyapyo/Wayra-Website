"""Unit tests of the archive views"""
from django.test import TestCase
from django.urls import reverse

from portfolio.models import Company, Individual, User, Portfolio_Company, Founder, InvestorCompany, InvestorIndividual
from portfolio.tests.helpers import LogInTester, reverse_with_next
from django.http import HttpResponse
from portfolio.tests.helpers import set_session_variables, set_session_archived_company_filter_variable, set_session_archived_individual_filter_variable


class ArchiveViewTestCase(TestCase):
    """Unit tests of the archive view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/default_portfolio_company.json",
        "portfolio/tests/fixtures/other_companies.json",
        "portfolio/tests/fixtures/other_portfolio_companies.json",
        "portfolio/tests/fixtures/default_investor_company.json",
        "portfolio/tests/fixtures/other_investor_companies.json",
        "portfolio/tests/fixtures/default_individual.json",
        "portfolio/tests/fixtures/other_individuals.json",
        "portfolio/tests/fixtures/default_founder.json",
        "portfolio/tests/fixtures/other_founders.json",
        "portfolio/tests/fixtures/default_investor_individual.json",
        "portfolio/tests/fixtures/other_investor_individuals.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('archive_page')
        self.search_url = reverse('archive_search')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        set_session_variables(self.client)

    def test_archive_url(self):
        self.assertEqual(self.url, '/archive_page/')

    def test_get_archive(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/archive_page.html')

    def test_get_archive_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # def test_get_archive_redirects_when_not_admin(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     redirect_url = reverse('dashboard')
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_archive_search_url(self):
        self.assertEqual(self.search_url, '/archive/search')

    def test_get_search_archive(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.search_url, data={'searchresult': 'w'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
    
    def test_get_search_archive_returns_correct_data(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.search_url, data={'searchresult': 'w'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        company_search_result = Company.objects.filter(name__contains="w", is_archived=True).values()
        individual_search_result = Individual.objects.filter(name__contains="w", is_archived=True).values()
        for company in company_search_result:
            self.assertContains(response, company.name)
        for individual in individual_search_result:
            self.assertContains(response, individual.name)
    
    #archive search test for different filter
    def test_get_search_archive_returns_correct_data_for_portfolio_companies_and_founders(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        set_session_archived_company_filter_variable(self.client, 2)
        set_session_archived_individual_filter_variable(self.client, 2)
        search = 'a'
        response = self.client.get(self.search_url, data={'searchresult': search})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        company_search_result = Portfolio_Company.objects.filter(name__contains=search,is_archived=True).values().order_by('id')
        individual_search_result = Individual.objects.filter(name__contains=search, is_archived=True).values()
        founder_individuals = Founder.objects.all()
        individual_search_result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), name__contains=search, is_archived=True).values().order_by('id')
        for company in company_search_result:
            self.assertContains(response, company.name)
        for individual in individual_search_result:
            self.assertContains(response, individual.name)

    def test_get_search_archive_returns_correct_data_for_portfolio_companies_and_founders(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        set_session_archived_company_filter_variable(self.client, 3)
        set_session_archived_individual_filter_variable(self.client, 3)
        search = 'a'
        response = self.client.get(self.search_url, data={'searchresult': search})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        investor_companies = InvestorCompany.objects.all()
        company_search_result = Company.objects.filter(id__in=investor_companies.values('company'),name__contains=search, is_archived=True).values().order_by('id')
        individual_search_result = InvestorIndividual.objects.filter(name__contains=search, is_archived=True).values().order_by('id')

        for company in company_search_result:
            self.assertContains(response, company.name)
        for individual in individual_search_result:
            self.assertContains(response, individual.name)
    
    def test_search_with_blank_query(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.search_url, {'searchresult': ''})
        self.assertEqual(response.status_code, 200)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("partials/search/search_results_table.html", template_names)
        self.assertNotContains(response, 'No Search Results Found.')

    def test_search_archive_without_results(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.search_url, {'searchresult': 'NonExistentCompany"$%#1234'})
        self.assertEqual(response.status_code, 200)
        templates = response.templates
        template_names = [template.name for template in templates]
        self.assertIn("partials/search/search_results_table.html", template_names)
        self.assertContains(response, 'No Search Results Found.')