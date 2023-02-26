from django.test import TestCase
from django.urls import reverse
from portfolio.models import Individual, ResidentialAddress, PastExperience, Founder, User
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm, FounderForm
from django_countries.fields import Country, LazyTypedChoiceField 
from phonenumber_field.phonenumber import PhoneNumber


class FounderCreateTestCase(TestCase):
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]
    
    
    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        self.url = reverse('founder_create')
        self.founder_data = {
            'name': "Ben", 
            "AngelListLink" : "https://www.AngelList.com",
            "CrunchbaseLink" : "https://www.Crunchbase.com",
            "LinkedInLink" : "https://www.LinkedIn.com",
            "Company" : "exampleCompany",
            "Position" : "examplePosition",
            "Email" : "test@gmail.com",
            "PrimaryNumber_0": "UK",
            "PrimaryNumber_1": "+447975777666",
            "SecondaryNumber_0": "UK",
            "SecondaryNumber_1": "+441325777655",
            "companyFounded": "startup",
            "additionalInformation": "Founder founded a startup firm."
        }
        self.address_data = {
            "address_line1" : "testAdress1",
            "address_line2" : "testAdress2",
            "postal_code" : "testCode",
            "city" : "testCity",
            "state" : "testState",
            "country" : Country("AD")
        }
        self.past_experience_data = [
            {
                'companyName': "Startup",
                'workTitle': "CEO",
                'start_year': 1995,
                'end_year': 1998, 
                'Description': "I am the CEO of Startup."
            },
            {
                'companyName': "Startup2",
                'workTitle': "Manager",
                'start_year': 2001,
                'end_year': 2020, 
                'Description': "I am the manager of Startup."
            }
        ]

    def test_founder_create_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'individual/founder_create.html')
        self.assertIsInstance(response.context['founderForm'], FounderForm)
        # self.assertIsInstance(response.context['addressForms'], AddressCreateForm)
        # self.assertIsInstance(response.context['pastExperienceForms'][0], PastExperienceForm)
        # self.assertIsInstance(response.context['pastExperienceForms'][1], PastExperienceForm)

    def test_founder_create_post(self):
        data = {
            'name': 'John Doe',
            'AngelListLink': 'https://angel.co/johndoe',
            'CrunchbaseLink': 'https://www.crunchbase.com/person/john-doe',
            'LinkedInLink': 'https://www.linkedin.com/in/john-doe/',
            'Company': 'Example Company',
            'Position': 'CEO',
            'Email': 'johndoe@example.com',
            'PrimaryNumber_0': '+1',
            'PrimaryNumber_1': '+447975777666',
            'SecondaryNumber_0': '+1',
            'SecondaryNumber_1': '+447975777666',
            'companyFounded': 'startup',
            'additionalInformation': 'Some additional information',
        }
        # Modify the phone number fields to use valid phone numbers
        form = FounderForm(data=data)
        if form.is_valid():
            before_count = Founder.objects.count()
            response = self.client.post(self.url, data, follow=True)
            after_count = Founder.objects.count()
            self.assertEqual(before_count+1, after_count)