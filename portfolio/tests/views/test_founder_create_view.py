from django.test import TestCase
from django.urls import reverse
from portfolio.models import ResidentialAddress, PastExperience, Founder, User
from portfolio.forms import AddressCreateForm, PastExperienceForm, FounderForm
from django_countries.fields import Country
from django_countries.fields import Country
from portfolio.tests.helpers import reverse_with_next



class FounderCreateTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]
    
    
    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('founder_create')
        
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

    def test_founder_create_url(self):
        self.assertEqual(self.url, '/individual_page/founder_create/')

    def test_founder_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/founder_create.html')
        self.assertIsInstance(response.context['founderForm'], FounderForm)
        self.assertIsInstance(response.context['addressForms'], AddressCreateForm)
        self.assertIsInstance(response.context['pastExperienceForms'][0], PastExperienceForm)
        self.assertIsInstance(response.context['pastExperienceForms'][1], PastExperienceForm)

    def test_founder_create_post(self):
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        redirect_url = reverse('individual_page')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirect_when_user_access_founder_create_not_loggedin(self):
        self.client.logout()
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    def test_post_founder_request_with_blank_name(self):
        self.post_input['form1-name'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_angellist_link_invalid(self):
        self.post_input['form1-AngelListLink'] = "hi"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)

    def test_post_crunchbase_link_invalid(self):
        self.post_input['form1-CrunchbaseLink'] = "hi"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_linkedin_link_invalid(self):
        self.post_input['form1-LinkedInLink'] = "hi"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_company_cannot_be_blank(self):
        self.post_input['form1-Company'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_position_cannot_be_blank(self):
        self.post_input['form1-Position'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_email_cannot_be_blank(self):
        self.post_input['form1-Email'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_email_cannot_be_invalid(self):
        self.post_input['form1-Email'] = "hi"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_primary_number_cannot_be_invalid(self):
        self.post_input['form1-PrimaryNumber_1'] = "02"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_secondary_number_can_be_blank(self):
        self.post_input['form1-SecondaryNumber_1'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)
    
    def test_post_company_founded_cannot_be_blank(self):
        self.post_input['form1-companyFounded'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)

    def test_post_additional_information_can_be_blank(self):
        self.post_input['form1-additionalInformation'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)
    
    def test_post_address_line_1_cannot_be_blank(self):
        self.post_input['form2-address_line1'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_address_line_2_cannot_be_blank(self):
        self.post_input['form1-address_line2'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)
    
    def test_post_postal_code_cannot_be_blank(self):
        self.post_input['form2-postal_code'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_city_cannot_be_blank(self):
        self.post_input['form2-city'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_state_can_be_blank(self):
        self.post_input['form2-state'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)
    
    def test_post_country_cannot_be_invalid(self):
        self.post_input['form2-country'] = "hi"
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_country_cannot_be_blank(self):
        self.post_input['form2-country'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_past_experience_companyName_cannot_be_blank(self):
        self.post_input['0-companyName'] = ""
        self.post_input['1-companyName'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_past_experience_workTitle_cannot_be_blank(self):
        self.post_input['0-workTitle'] = ""
        self.post_input['1-workTitle'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_past_experience_start_year_cannot_be_blank(self):
        self.post_input['0-start_year'] = ""
        self.post_input['1-start_year'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_past_experience_end_year_can_be_blank(self):
        self.post_input['0-end_year'] = ""
        self.post_input['1-end_year'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(before_count2, after_count2)
        self.assertEqual(before_count3, after_count3)
        self.assertEqual(response.status_code, 200)
    
    def test_post_past_description_can_be_blank(self):
        self.post_input['0-Description'] = ""
        self.post_input['1-Description'] = ""
        before_count = Founder.objects.count()
        before_count2 = ResidentialAddress.objects.count()
        before_count3 = PastExperience.objects.count()
        response = self.client.post(self.url, self.post_input)
        after_count = Founder.objects.count()
        after_count2 = ResidentialAddress.objects.count()
        after_count3 = PastExperience.objects.count()
        self.assertEqual(before_count+1, after_count)
        self.assertEqual(before_count2+1, after_count2)
        self.assertEqual(before_count3+2, after_count3)
        self.assertEqual(response.status_code, 302)
    

    



    

    


    

    
    
    

        


        
