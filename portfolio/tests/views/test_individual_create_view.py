"""Tests of the sign up view."""
from django.test import TestCase
from django.urls import reverse
from portfolio.models import Individual, ResidentialAddress
from django_countries.fields import Country
from portfolio.forms import IndividualCreateForm, AddressCreateForm


class IndividualCreateViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('individual_create')
        self.post_input = {
            "form1-AngelListLink": "https://www.AngelList.com",
            "form1-CrunchbaseLink": "https://www.Crunchbase.com",
            "form1-LinkedInLink": "https://www.LinkedIn.com",
            "form1-Company": "exampleCompany",
            "form1-Position": "examplePosition",
            "form1-Email": "test@gmail.com",
            "form1-PrimaryNumber_0": "UK",
            "form1-PrimaryNumber_1": "+447975777666",
            "form1-SecondaryNumber_0": "UK",
            "form1-SecondaryNumber_1": "+441325777655",
            "form2-address_line1": "testAdress1",
            "form2-address_line2": "testAdress2",
            "form2-postal_code": "testCode",
            "form2-city": "testCity",
            "form2-state": "testState",
            "form2-country": Country("AD")
        }

    def test_individual_create_view_url(self):
        self.assertEqual(self.url, '/individual_page/individual_create/')

    # Tests if the individual_create_view page renders correctly with the correct forms and html
    def test_get_individual_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        individual_form = response.context['individualForm']
        self.assertTrue(isinstance(individual_form, IndividualCreateForm))
        adress_form = response.context['addressForms']
        self.assertTrue(isinstance(adress_form, AddressCreateForm))
        self.assertFalse(adress_form.is_bound)
        self.assertFalse(individual_form.is_bound)

    def test_unsuccessful_individual_create_view_due_to_individual_form(self):
        self.post_input['form1-AngelListLink'] = 'A'
        before_count = Individual.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Individual.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        form = response.context['individualForm']
        self.assertTrue(isinstance(form, IndividualCreateForm))
        self.assertTrue(form.is_bound)

    def test_unsuccessful_individual_create_view_due_to_adress_form(self):
        self.post_input['form2-country'] = Country("false")
        before_count = ResidentialAddress.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = ResidentialAddress.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/individual_create.html')
        form = response.context['addressForms']
        self.assertTrue(isinstance(form, AddressCreateForm))
        self.assertTrue(form.is_bound)

    # Tests if an successful individual_create produces the desired results
    # def test_successful_individual_create_view(self):
    #     before_count_individual = Individual.objects.count()
    #     before_count_address = ResidentialAddress.objects.count()
    #     self.client.post(self.url, self.post_input)
    #     after_count_individual = ResidentialAddress.objects.count()
    #     after_count_adress = ResidentialAddress.objects.count()
    #
    #     self.assertEqual(after_count_adress, before_count_individual + 1)
    #     individual = Individual.objects.get(Company='exampleCompany')
    #     self.assertEqual(individual.AngelListLink, "https://www.AngelList.com")
    #     self.assertEqual(individual.CrunchbaseLink, "https://www.Crunchbase.com")
    #     self.assertEqual(individual.LinkedInLink, "https://www.LinkedIn.com")
    #     self.assertEqual(individual.Company, "exampleCompany")
    #     self.assertEqual(individual.Position, "examplePosition")
    #     self.assertEqual(individual.Email, "test@gmail.com")
    #     self.assertEqual(individual.PrimaryNumber, "+447975777666")
    #     self.assertEqual(individual.SecondaryNumber, "+441325777655")
    #
    #     self.assertEqual(after_count_individual, before_count_address + 1)
    #     residential_adress = ResidentialAddress.objects.get(address_line1='testAdress1')
    #     self.assertEqual(residential_adress.address_line1, "testAdress1")
    #     self.assertEqual(residential_adress.address_line2, "testAdress2")
    #     self.assertEqual(residential_adress.postal_code, "testCode")
    #     self.assertEqual(residential_adress.city, "testCity")
    #     self.assertEqual(residential_adress.state, "testState")
    #     self.assertEqual(residential_adress.country, Country("AD"))
