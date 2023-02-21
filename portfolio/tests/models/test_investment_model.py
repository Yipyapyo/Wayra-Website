from django.test import TestCase
from django.core.exceptions import ValidationError
from portfolio.models.investment_model import Investment
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.investor_individual_model import InvestorIndividual
from portfolio.models.company_model import PortfolioCompany
from phonenumber_field.phonenumber import PhoneNumber
from django.utils import timezone


class InvestmentModelTestCase(TestCase):
    """Unit test for the investment model"""
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
        self.investment = Investment.objects.create(
            typeOfFoundingRounds= "Seed round",
            moneyRaised = 10,
            dateInvested=timezone.now(),
        )
        
    def test_investor_company_many_to_many_field(self):
        self.investment.investor.add(self.InvestorCompany)
        self.assertEqual(self.investment.investor.count(), 1)
        self.assertIn(self.InvestorCompany, self.investment.investor.all())

    # Assert an investment is valid
    def _assert_investment_is_valid(self):
        try:
            self.investment.full_clean()
        except ValidationError:
            self.fail('Test individual is not valid.')

    # Assert an investment is invalid
    def _assert_investment_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.investment.full_clean()
