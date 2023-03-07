
from django.test import TestCase
from django.urls import reverse
from portfolio.models import ResidentialAddress, PastExperience, User
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.forms import AddressCreateForm, PastExperienceForm
from portfolio.forms.investor_individual_form import InvestorIndividualForm
from django_countries.fields import Country
from portfolio.tests.helpers import reverse_with_next, set_session_variables



class InvestorIndividualCreateTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]
    
    
    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('investor_individual_create')
        set_session_variables(self.client)
        
        self.post_input = {
            "form1-name": "Jemma Doe",
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
            "form1-NumberOfPortfolioCompanies": 5,
            "form1-NumberOfPersonalInvestments": 5,
            "form1-NumberOfPartnerInvestments": 5,
            "form1-PartOfIncubator": False,
            "form1-NumberOfExits": 5,
            "form2-address_line1": "testAdress1",
            "form2-address_line2": "testAdress2",
            "form2-postal_code": "testCode",
            "form2-city": "testCity",
            "form2-state": "testState",
            "form2-country": Country("AD"),
            "0-companyName": "exampleCompany",
            "0-workTitle" : "exampleWork",
            "0-start_year" : 2033,
            "0-end_year" : 2035,
            "0-Description" : "testCase",
            "1-companyName": "exampleCompany2",
            "1-workTitle" : "exampleWork2",
            "1-start_year" : 2034,
            "1-end_year" : 2036,
            "1-Description" : "testCase2"
        }

    def test_investor_individual_create_url(self):
        self.assertEqual(self.url, '/individual_page/investor_individual_create/')

    def test_investor_individual_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/investor_individual_create.html')
        self.assertIsInstance(response.context['investorIndividualForm'], InvestorIndividualForm)
        self.assertIsInstance(response.context['addressForms'], AddressCreateForm)
        self.assertIsInstance(response.context['pastExperienceForms'][0], PastExperienceForm)
        self.assertIsInstance(response.context['pastExperienceForms'][1], PastExperienceForm)

    def test_investor_individual_create_post(self):
        before_count = InvestorIndividual.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = InvestorIndividual.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        redirect_url = reverse('individual_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirect_when_user_access_investor_individual_create_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_post_investor_individual_request_with_blank_name(self):
        self.post_input['form1-name'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_angellist_link_invalid(self):
        self.post_input['form1-AngelListLink'] = "hi"
        self.cannot_create_investor_individual()

    def test_post_crunchbase_link_invalid(self):
        self.post_input['form1-CrunchbaseLink'] = "hi"
        self.cannot_create_investor_individual()
    
    def test_post_linkedin_link_invalid(self):
        self.post_input['form1-LinkedInLink'] = "hi"
        self.cannot_create_investor_individual()
    
    def test_post_company_cannot_be_blank(self):
        self.post_input['form1-Company'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_position_cannot_be_blank(self):
        self.post_input['form1-Position'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_email_cannot_be_blank(self):
        self.post_input['form1-Email'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_email_cannot_be_invalid(self):
        self.post_input['form1-Email'] = "hi"
        self.cannot_create_investor_individual()
    
    def test_post_primary_number_cannot_be_invalid(self):
        self.post_input['form1-PrimaryNumber_1'] = "02"
        self.cannot_create_investor_individual()
    
    def test_post_secondary_number_can_be_blank(self):
        self.post_input['form1-SecondaryNumber_1'] = ""
        self.can_create_investor_individual()
    
    def test_post_number_of_portfolio_companies_cannot_be_blank(self):
        self.post_input['form1-NumberOfPortfolioCompanies'] = ""
        self.cannot_create_investor_individual()

    def test_post_number_of_personal_investments_cannot_be_blank(self):
        self.post_input['form1-NumberOfPersonalInvestments'] = ""
        self.cannot_create_investor_individual()

    def test_post_number_of_partner_investments_cannot_be_blank(self):
        self.post_input['form1-NumberOfPartnerInvestments'] = ""
        self.cannot_create_investor_individual()

    def test_post_part_of_incubator_can_be_blank(self):
        self.post_input['form1-PartOfIncubator'] = ""
        self.can_create_investor_individual()

    def test_post_number_of_exits_cannot_be_blank(self):
        self.post_input['form1-NumberOfExits'] = ""
        self.cannot_create_investor_individual()

    def test_post_address_line_1_cannot_be_blank(self):
        self.post_input['form2-address_line1'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_address_line_2_cannot_be_blank(self):
        self.post_input['form2-address_line2'] = ""
        self.can_create_investor_individual()
    
    def test_post_postal_code_cannot_be_blank(self):
        self.post_input['form2-postal_code'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_city_cannot_be_blank(self):
        self.post_input['form2-city'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_state_can_be_blank(self):
        self.post_input['form2-state'] = ""
        self.can_create_investor_individual()
    
    def test_post_country_cannot_be_invalid(self):
        self.post_input['form2-country'] = "hi"
        self.cannot_create_investor_individual()
    
    def test_post_country_cannot_be_blank(self):
        self.post_input['form2-country'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_past_experience_companyName_cannot_be_blank(self):
        self.post_input['0-companyName'] = ""
        self.post_input['1-companyName'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_past_experience_workTitle_cannot_be_blank(self):
        self.post_input['0-workTitle'] = ""
        self.post_input['1-workTitle'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_past_experience_start_year_cannot_be_blank(self):
        self.post_input['0-start_year'] = ""
        self.post_input['1-start_year'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_past_experience_end_year_cannot_be_blank(self):
        self.post_input['0-end_year'] = ""
        self.post_input['1-end_year'] = ""
        self.cannot_create_investor_individual()
    
    def test_post_past_description_can_be_blank(self):
        self.post_input['0-Description'] = ""
        self.post_input['1-Description'] = ""
        self.can_create_investor_individual()

#Helper functions
    def can_create_investor_individual(self):
        before_count = InvestorIndividual.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = InvestorIndividual.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)

    def cannot_create_investor_individual(self):
        before_count = InvestorIndividual.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = InvestorIndividual.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)