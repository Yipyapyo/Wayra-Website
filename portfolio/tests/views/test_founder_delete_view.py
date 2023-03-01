"""Unit tests for the founder delete page."""
from django.test import TestCase
from django.urls import reverse
from portfolio.models import Founder, User
from portfolio.forms import IndividualCreateForm, AddressCreateForm, PastExperienceForm, FounderForm
from django_countries.fields import Country, LazyTypedChoiceField 
from phonenumber_field.phonenumber import PhoneNumber
from django_countries.fields import Country

class FounderDeleteTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.client.login(email=self.user.email, password="Password123")
        