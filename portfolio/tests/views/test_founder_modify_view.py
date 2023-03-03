from django.test import TestCase
from django.urls import reverse
from portfolio.models import ResidentialAddress, PastExperience, Founder, User
from portfolio.forms import AddressCreateForm, PastExperienceForm, FounderForm
from django_countries.fields import Country
from django_countries.fields import Country
from portfolio.tests.helpers import reverse_with_next

class FounderModifyTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")

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
            "form1-companyFounded": "Companyname",
            "form1-additionalInformation": "Info",
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
            "1-Description" : "testCase2",
        }

        self.url2 = reverse('founder_create')
        self.client.post(self.url2, self.post_input)
        self.listUsed = Founder.objects.filter(name="Jemma Doe")[0]
        self.url = reverse('founder_modify', kwargs={'id': self.listUsed.id})
    
    def test_founder_modify_url(self):
        self.assertEqual(self.url, '/individual_page/{}/modifyFounder/'.format(self.listUsed.id))
    
    def test_redirect_when_user_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_post_founder_update_with_blank_name(self):
        self.post_input['form1-name'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(Company="exampleCompany")[0]
        self.assertEqual(founder.name, "Jemma Doe")
    
    def test_post_founder_update_angellist_link_invalid(self):
        self.post_input['form1-AngelListLink'] = "hi"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.AngelListLink, "https://www.AngelList.com")

    def test_post_founder_udpate_crunchbase_link_invalid(self):
        self.post_input['form1-CrunchbaseLink'] = "hi"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.CrunchbaseLink, "https://www.Crunchbase.com")

    def test_post_founder_update_linkedin_link_invalid(self):
        self.post_input['form1-LinkedInLink'] = "hi"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.LinkedInLink, "https://www.LinkedIn.com")

    def test_post_founder_update_company_cannot_be_blank(self):
        self.post_input['form1-Company'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.Company, "exampleCompany")
    
    def test_post_founder_update_position_cannot_be_blank(self):
        self.post_input['form1-Position'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.Position, "examplePosition")
    
    def test_post_founder_update_email_cannot_be_blank(self):
        self.post_input['form1-Email'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.Email, "test@gmail.com")
    
    def test_post_founder_update_email_cannot_be_invalid(self):
        self.post_input['form1-Email'] = "hi"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.Email, "test@gmail.com")
    
    def test_post_founder_update_primary_number_cannot_be_invalid(self):
        self.post_input['form1-PrimaryNumber_1'] = "02"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.PrimaryNumber, "+447975777666")
    
    def test_post_founder_update_company_founded_cannot_be_blank(self):
        self.post_input['form1-companyFounded'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        founder = Founder.objects.filter(name="Jemma Doe")[0]
        self.assertEqual(founder.companyFounded, "Companyname")
    
    def test_address_update_post_address_line_1_cannot_be_blank(self):
        self.post_input['form2-address_line1'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.address_line1, "testAdress1")
    
    def test_post_address_line_2_cannot_be_blank(self):
        self.post_input['form1-address_line2'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.address_line2, "testAdress2")
    
    def test_post_postal_code_cannot_be_blank(self):
        self.post_input['form2-postal_code'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.postal_code, "testCode")
    
    def test_post_city_cannot_be_blank(self):
        self.post_input['form2-city'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.city, "testCity")
    
    
    def test_post_country_cannot_be_invalid(self):
        self.post_input['form2-country'] = "hi"
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.country, Country(code="AD"))
    
    
    def test_post_country_cannot_be_blank(self):
        self.post_input['form2-country'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        address = ResidentialAddress.objects.filter(address_line1="testAdress1")[0]
        self.assertEqual(address.country, Country(code="AD"))
    
    def test_post_past_experience_companyName_cannot_be_blank(self):
        self.post_input['0-companyName'] = ""
        self.post_input['1-companyName'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        pastExp1 = PastExperience.objects.filter(companyName="exampleCompany")[0]
        pastExp2 = PastExperience.objects.filter(companyName="exampleCompany2")[0]
        self.assertEqual(pastExp1.companyName, "exampleCompany")
        self.assertEqual(pastExp2.companyName, "exampleCompany2")
    
    def test_post_past_experience_workTitle_cannot_be_blank(self):
        self.post_input['0-workTitle'] = ""
        self.post_input['1-workTitle'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        pastExp1 = PastExperience.objects.filter(companyName="exampleCompany")[0]
        pastExp2 = PastExperience.objects.filter(companyName="exampleCompany2")[0]
        self.assertEqual(pastExp1.workTitle, "exampleWork")
        self.assertEqual(pastExp2.workTitle, "exampleWork2")
    
    def test_post_past_experience_start_year_cannot_be_blank(self):
        self.post_input['0-start_year'] = ""
        self.post_input['1-start_year'] = ""
        response = self.client.post(self.url, self.post_input)
        self.assertEqual(response.status_code, 200)
        pastExp1 = PastExperience.objects.filter(companyName="exampleCompany")[0]
        pastExp2 = PastExperience.objects.filter(companyName="exampleCompany2")[0]
        self.assertEqual(pastExp1.start_year, 2033)
        self.assertEqual(pastExp2.start_year, 2034)
    
    
    
    

    



    

    


    

    
    
    

        


        
