"""Founder form """
from django import forms
from django.forms.fields import URLField
from django.test import TestCase
from phonenumber_field.formfields import PhoneNumberField
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.forms.investor_individual_form import InvestorIndividualForm

class InvestorIndividualFormTestCase(TestCase):
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
             "NumberOfPortfolioCompanies": 5,
             "NumberOfPersonalInvestments": 5,
             "NumberOfPartnerInvestments": 5,
             "PartOfIncubator": False,
             "NumberOfExits": 5
        }
    
    def test_valid_founder_form(self):
        form = InvestorIndividualForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_has_necessary_fields(self):
        form = InvestorIndividualForm()
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
        self.assertIn('NumberOfPortfolioCompanies', form.fields)
        self.assertTrue(isinstance(form.fields['NumberOfPortfolioCompanies'], forms.IntegerField))
        self.assertIn('NumberOfPersonalInvestments', form.fields)
        self.assertTrue(isinstance(form.fields['NumberOfPersonalInvestments'], forms.IntegerField))
        self.assertIn('NumberOfPartnerInvestments', form.fields)
        self.assertTrue(isinstance(form.fields['NumberOfPartnerInvestments'], forms.IntegerField))
        self.assertIn('PartOfIncubator', form.fields)
        self.assertTrue(isinstance(form.fields['PartOfIncubator'], forms.BooleanField))
        self.assertIn('NumberOfExits', form.fields)
        self.assertTrue(isinstance(form.fields['NumberOfExits'], forms.IntegerField))

    
    def test_form_saves_correctly(self):
        form = InvestorIndividualForm(data=self.form_input)
        before_count = InvestorIndividual.objects.count()
        form.save()
        after_count = InvestorIndividual.objects.count()
        self.assertEqual(after_count, before_count+1)
        investor_individual = InvestorIndividual.objects.get(Company='exampleCompany')
        self.assertEqual(investor_individual.AngelListLink, "https://www.AngelList.com")
        self.assertEqual(investor_individual.CrunchbaseLink, "https://www.Crunchbase.com")
        self.assertEqual(investor_individual.LinkedInLink, "https://www.LinkedIn.com")
        self.assertEqual(investor_individual.Company, "exampleCompany")
        self.assertEqual(investor_individual.Position, "examplePosition")
        self.assertEqual(investor_individual.Email, "test@gmail.com")
        self.assertEqual(investor_individual.PrimaryNumber, "+447975777666")
        self.assertEqual(investor_individual.SecondaryNumber, "+441325777655")
        self.assertEqual(investor_individual.NumberOfPortfolioCompanies, 5)
        self.assertEqual(investor_individual.NumberOfPersonalInvestments, 5)
        self.assertEqual(investor_individual.NumberOfPartnerInvestments, 5)
        self.assertEqual(investor_individual.PartOfIncubator, False)
        self.assertEqual(investor_individual.NumberOfExits, 5)
        