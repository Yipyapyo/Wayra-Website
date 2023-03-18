"""Tests of the Individual views."""
from django.test import TestCase
from django.urls import reverse
from portfolio.models import Individual, Founder, User, InvestorIndividual, Investor
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import Country
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm
from portfolio.tests.helpers import reverse_with_next, set_session_variables, set_session_individual_filter_variable
from django.http import HttpResponse



class IndividualProfileViewTestCase(TestCase):
    """Tests of the Individual views."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_individual.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('individual_profile', kwargs={'id':1})
        set_session_variables(self.client)

    def test_individual_profile_view_url(self):
        self.assertEqual(self.url, '/individual_profile_page/1/')

    def test_get_individual_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_about_page.html')

    def test_redirect_when_user_access_investor_individual_profile_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirects_when_individual_archived_and_not_admin(self):
        self.client.login(email=self.user.email, password="Password123")
        individual = Individual.objects.get(id=1)
        individual.is_archived = True
        individual.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

class IndividualArchiveViewTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_individual.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('archive_individual', kwargs={'id':1})
        set_session_variables(self.client)

    def test_individual_archive_view_url(self):
        self.assertEqual(self.url, '/individual_page/archive/1')

    def test_get_individual_archive_view(self):
        individual = Individual.objects.get(id=1)
        before_archive = individual.is_archived
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        individual = Individual.objects.get(id=1)
        after_archive = individual.is_archived
        self.assertEqual(before_archive, False)
        self.assertEqual(after_archive, True)
        self.assertNotEqual(before_archive, after_archive)

    def test_redirect_when_user_access_investor_individual_archive_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)




class IndividualUnarchiveViewTestCase(TestCase):
    """Tests for the individual unarchive views."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_individual.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('unarchive_individual', kwargs={'id':1})
        set_session_variables(self.client)

    def test_individual_archive_view_url(self):
        self.assertEqual(self.url, '/individual_page/unarchive/1')

    def test_get_individual_unarchive_view(self):
        response = self.client.get(reverse('archive_individual', kwargs={'id':1}))
        individual = Individual.objects.get(id=1)
        before_archive = individual.is_archived
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        individual = Individual.objects.get(id=1)
        after_archive = individual.is_archived
        self.assertEqual(before_archive, True)
        self.assertEqual(after_archive, False)
        self.assertNotEqual(before_archive, after_archive)

    def test_redirect_when_user_access_investor_individual_unarchive_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
class IndividualFilterViewTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_individual.json",
        "portfolio/tests/fixtures/other_individuals.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/other_companies.json",
        "portfolio/tests/fixtures/default_founder.json",
        "portfolio/tests/fixtures/other_founders.json",
        "portfolio/tests/fixtures/default_investor_individual.json",
        "portfolio/tests/fixtures/other_investor_individuals.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('change_individual_filter')
        set_session_variables(self.client)

    def test_individual_filter_view_url(self):
        self.assertEqual(self.url, '/change_individual_filter/')

    def test_redirect_when_user_access_investor_individual_filternot_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_individual_change_filter(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'filter_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_get_change_filter_returns_correct_data_for_all_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'filter_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        individual_search_result = Individual.objects.filter(is_archived=False).values()
        for individual in individual_search_result:
            self.assertContains(response, individual['name'])
        self.assertEqual(len(individual_search_result), 5)
        
    def test_get_change_filter_returns_correct_data_for_founder_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_individual_filter_variable(self.client, 2)
        response = self.client.get(self.url, data={'filter_number': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        founder_individuals = Founder.objects.all()
        test_result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), is_archived=False).order_by('id')
        for individual in test_result:
            self.assertContains(response, individual.name)
        self.assertEqual(len(test_result), 2)
    
    def test_get_change_filter_returns_correct_data_for_investor_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_individual_filter_variable(self.client, 3)
        response = self.client.get(self.url, data={'filter_number': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        investors = Investor.objects.all()
        test_result = Individual.objects.filter(id__in=investors.values('individual'), is_archived=False).order_by('id')
        for individual in test_result:
            self.assertContains(response, individual.name)
        self.assertEqual(len(test_result), 3)



class IndividualLayoutViewTestCase(TestCase):
    """Tests for the individual layout view."""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
        "portfolio/tests/fixtures/default_individual.json",
        "portfolio/tests/fixtures/other_individuals.json",
        "portfolio/tests/fixtures/default_company.json",
        "portfolio/tests/fixtures/other_companies.json",
        "portfolio/tests/fixtures/default_founder.json",
        "portfolio/tests/fixtures/other_founders.json",
        "portfolio/tests/fixtures/default_investor_individual.json",
        "portfolio/tests/fixtures/other_investor_individuals.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('change_individual_layout')
        set_session_variables(self.client)

    def test_individual_layout_view_url(self):
        self.assertEqual(self.url, '/change_individual_layout/')

    def test_redirect_when_user_access_investor_individual_layout_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_change_individual_layout(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'layout_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session['individual_layout']), 1)

    def test_get_change_layout_returns_correct_data_for_all_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, data={'layout_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        individual_search_result = Individual.objects.filter(is_archived=False).values()
        self.assertEqual(len(individual_search_result), 5)

    def test_get_change_layout_returns_correct_data_for_portfolio_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_individual_filter_variable(self.client, 2)
        response = self.client.get(self.url, data={'layout_number': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        founder_individuals = Founder.objects.all()
        result = Individual.objects.filter(id__in=founder_individuals.values('individualFounder'), is_archived=False).order_by('id')
        self.assertEqual(len(result), 2)

    def test_get_change_filter_returns_correct_data_for_investor_individuals(self):
        self.client.login(email=self.user.email, password="Password123")
        set_session_individual_filter_variable(self.client, 3)
        response = self.client.get(self.url, data={'layout_number': 3})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse) 
        investors = Investor.objects.all()
        test_result = Individual.objects.filter(id__in=investors.values('individual'), is_archived=False).order_by('id')
        self.assertEqual(len(test_result), 3)