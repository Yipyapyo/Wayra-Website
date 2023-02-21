"""Unit tests for the investment form"""
from django import forms
from django.test import TestCase
from portfolio.models import Investment
from portfolio.forms import InvestmentForm
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.models.company_model import PortfolioCompany
from phonenumber_field.phonenumber import PhoneNumber
from django.utils import timezone

class InvestmentFormTestCase(TestCase):
    def setUp(self):
        self.InvestorIndividual = InvestorIndividual.objects.create(
             AngelListLink = "https://www.AngelList.com",
             CrunchbaseLink = "https://www.Crunchbase.com",
             LinkedInLink = "https://www.LinkedIn.com",
             Company = "exampleCompany",
             Position = "examplePosition",
             Email = "test@gmail.com",
             PrimaryNumber = PhoneNumber.from_string("+447975777666"),
             SecondaryNumber = PhoneNumber.from_string("+441325777655"),
             NumberOfPortfolioCompanies = 5,
             NumberOfPersonalInvestments = 5,
             NumberOfPartnerInvestments = 5,
             PartOfIncubator = False,
             NumberOfExits = 5
        )
        self.PortfolioCompany = PortfolioCompany.objects.create(
            name="Facebook",
            company_registration_number="00000000",
            trading_names="Defaul",
            previous_names="Google",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now(),
            wayra_number= "12345",
        )

        self.InvestorCompany = InvestorCompany.objects.create(
            name="Nike",
            company_registration_number="00000000",
            trading_names="NBA",
            previous_names="Amazon",
            jurisdiction="United Kingdom",
            incorporation_date=timezone.now(),
            AngelListLink = "https://www.AngelList.com",
            CrunchbaseLink = "https://www.Crunchbase.com",
            LinkedInLink = "https://www.LinkedIn.com",
            Type = "VC",
            NumberOfInvestments = 5,
            NumberOfLeadInvestments = 5,
            NumberOfDiversityInvestments = 3,
            NumberOfExits = 2,
        )

        self.form_input = {
            "investor": [self.InvestorCompany.pk],
            "individualInvestor": [self.InvestorIndividual.pk],
            "startup": [self.PortfolioCompany.pk],
            "typeOfFoundingRounds": "Seed round",
            "moneyRaised": 10,
        }

    def test_investment_form_valid(self):
        form = InvestmentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = InvestmentForm()
        self.assertIn('investor', form.fields)
        investor_field = form.fields['investor']
        self.assertTrue(isinstance(investor_field, forms.ModelMultipleChoiceField))
        self.assertIn('individualInvestor', form.fields)
        individualInvestor_field = form.fields['individualInvestor']
        self.assertTrue(isinstance(individualInvestor_field, forms.ModelMultipleChoiceField))
        self.assertIn('startup', form.fields)
        startup_field = form.fields['startup']
        self.assertTrue(isinstance(startup_field, forms.ModelMultipleChoiceField))
        self.assertIn('typeOfFoundingRounds', form.fields)
        foundingRounds_field = form.fields['typeOfFoundingRounds']
        self.assertTrue(isinstance(foundingRounds_field, forms.ChoiceField))
        self.assertIn('moneyRaised', form.fields)
        moneyRaised_field = form.fields['moneyRaised']
        self.assertTrue(isinstance(moneyRaised_field, forms.DecimalField))

    def test_form_saves_correctly(self):
        form = InvestmentForm(data=self.form_input)
        before_count = Investment.objects.count()
        form.save()
        after_count = Investment.objects.count()
        self.assertEqual(after_count, before_count+1)
        investment = Investment.objects.get(moneyRaised=10)
        investors = list(investment.investor.all())
        self.assertEqual(len(investors), 1)
        self.assertEqual(investors[0], self.InvestorCompany)
    
        individuals = list(investment.individualInvestor.all())
        self.assertEqual(len(individuals), 1)
        self.assertEqual(individuals[0], self.InvestorIndividual)
    
        startups = list(investment.startup.all())
        self.assertEqual(len(startups), 1)
        self.assertEqual(startups[0], self.PortfolioCompany)
        self.assertEqual(investment.typeOfFoundingRounds, "Seed round")
        self.assertEqual(investment.moneyRaised, 10)