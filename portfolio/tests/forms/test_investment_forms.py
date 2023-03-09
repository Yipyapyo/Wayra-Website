from django.test import TestCase

from portfolio.models import Company, Portfolio_Company, InvestorCompany


class InvestmentFormTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(id=1)
        self.form_input = {'investor': self.investorCompany,
                           'startup': self.portfolioCompany,
                           'typeOfFoundingRounds': '',
                           'intestmentAmount': 10_000_000,
                           'dateInvested': '2023-03-05',
        }

    def test_valid_investment_create_form(self):
        pass

    def test_form_has_necessary_fields(self):
        pass

    def test_forms_uses_model_validation(self):
        pass

    def test_form_must_save_correctly(self):
        pass

