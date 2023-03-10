"""Founder form """
from django import forms
from django.forms.fields import URLField
from django.test import TestCase
from phonenumber_field.formfields import PhoneNumberField
from portfolio.models import Founder
from portfolio.forms import FounderForm

class FounderFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            "name": "Ben", 
            "AngelListLink" : "https://www.AngelList.com",
             "CrunchbaseLink" : "https://www.Crunchbase.com",
             "LinkedInLink" : "https://www.LinkedIn.com",
             "Company" : "exampleCompany",
             "Position" : "examplePosition",
             "Email" : "test@gmail.com",
             "PrimaryNumber_0" : "UK",
             "PrimaryNumber_1" : "+447975777666",
             "SecondaryNumber_0" : "UK",
             "SecondaryNumber_1" : "+441325777655",
             "companyFounded": "startup",
             "additionalInformation": "Founder founded a startup firm."
        }
    
    def test_valid_founder_form(self):
        form = FounderForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = FounderForm()
        self.assertIn("name", form.fields)
        self.assertTrue(isinstance(form.fields['name'], forms.CharField))
        self.assertIn("AngelListLink", form.fields)
        self.assertTrue(isinstance(form.fields['AngelListLink'], URLField))
        self.assertIn("CrunchbaseLink", form.fields)
        self.assertTrue(isinstance(form.fields['CrunchbaseLink'], URLField))
        self.assertIn("LinkedInLink", form.fields)
        self.assertTrue(isinstance(form.fields['LinkedInLink'], URLField))
        self.assertIn("Company", form.fields)
        self.assertIn("Position", form.fields)
        self.assertIn('Email', form.fields)
        self.assertTrue(isinstance(form.fields['Email'], forms.EmailField))
        self.assertIn('PrimaryNumber', form.fields)
        self.assertTrue(isinstance(form.fields['PrimaryNumber'], PhoneNumberField))
        self.assertIn('SecondaryNumber', form.fields)
        self.assertTrue(isinstance(form.fields['SecondaryNumber'], PhoneNumberField))
        self.assertIn('companyFounded', form.fields)
        self.assertTrue(isinstance(form.fields['companyFounded'], forms.CharField))
        self.assertIn('additionalInformation', form.fields)
        self.assertTrue(isinstance(form.fields['additionalInformation'], forms.CharField))
    
    def test_form_saves_correctly(self):
        form = FounderForm(data=self.form_input)
        before_count = Founder.objects.count()
        form.save()
        after_count = Founder.objects.count()
        self.assertEqual(after_count, before_count+1)
        founder = Founder.objects.get(Company='exampleCompany')
        self.assertEqual(founder.AngelListLink, "https://www.AngelList.com")
        self.assertEqual(founder.CrunchbaseLink, "https://www.Crunchbase.com")
        self.assertEqual(founder.LinkedInLink, "https://www.LinkedIn.com")
        self.assertEqual(founder.Company, "exampleCompany")
        self.assertEqual(founder.Position, "examplePosition")
        self.assertEqual(founder.Email, "test@gmail.com")
        self.assertEqual(founder.PrimaryNumber, "+447975777666")
        self.assertEqual(founder.SecondaryNumber, "+441325777655")
        self.assertEqual(founder.companyFounded, "startup")
        self.assertEqual(founder.additionalInformation, "Founder founded a startup firm.")
        