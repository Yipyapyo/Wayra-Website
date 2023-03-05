from django.test import TestCase
from django.utils import timezone

from portfolio.models import Company, Portfolio_Company, User, Investment, InvestorCompany
from portfolio.tests.helpers import LogInTester


class InvestmentCreateViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
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
                           'typeOfFoundingRounds': 'Series A',
                           'intestmentAmount': 10_000_000,
                           'dateInvested': '2023-03-05',
                           'contractRight': 'Default Contract Right',
                           }

    def test_create_investment_url(self):
        pass

    def test_get_create_investment_url(self):
        pass

    def test_get_create_investment_redirects_when_not_logged_in(self):
        pass

    def test_post_create_investment_redirects_when_not_logged_in(self):
        pass

    def test_successful_form(self):
        pass

    def test_unsuccessful_form(self):
        pass


class InvestmentUpdateViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(id=1)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolioCompany,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            dateExit=None,
            contractRight="Template - Contract - Right"
        )
        self.form_input = {'investor': self.defaultCompany,
                           'startup': self.portfolioCompany,
                           'typeOfFoundingRounds': 'Series A',
                           'intestmentAmount': 10_000_000,
                           'dateInvested': '2023-03-05',
                           'contractRight': 'Default Contract Right',
                           }

    def test_update_investment_url(self):
        pass

    def test_get_update_investment_url(self):
        pass

    def test_get_update_investment_redirects_when_not_logged_in(self):
        pass

    def test_post_update_investment_redirects_when_not_logged_in(self):
        pass

    def test_successful_form(self):
        pass

    def test_unsuccessful_form(self):
        pass


class InvestmentDeleteViewTestCase(TestCase, LogInTester):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_portfolio_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
        self.portfolioCompany = Portfolio_Company.objects.get(id=1)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolioCompany,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            dateExit=None,
            contractRight="Template - Contract - Right"
        )

    def test_delete_investment_url(self):
        pass

    def test_get_delete_investment_url(self):
        pass

    def test_get_delete_investment_redirects_when_not_logged_in(self):
        pass

    def test_post_delete_investment_redirects_when_not_logged_in(self):
        pass

    def test_successful_delete(self):
        pass


class InvestorCreateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.form_input = {
            'company': self.defaultCompany,
            'angelListLink': 'https://www.Angelist.com',
            'crunchbaseLink': 'https://www.crunchbase.com',
            'linkedInLink': 'https://www.linked-in.com',
            'classification': 'VC'
        }

    def test_create_investor_company_url(self):
        pass

    def test_get_create_investor_company_url(self):
        pass

    def test_get_create_investor_company_redirects_when_not_logged_in(self):
        pass

    def test_post_create_investor_company_redirects_when_not_logged_in(self):
        pass

    def test_successful_form(self):
        pass

    def test_unsuccessful_form(self):
        pass


class InvestorUpdateViewTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/default_company.json']

    def setUp(self) -> None:
        self.user = User.objects.get(email='john.doe@example.org')
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
        self.form_input = {
            'company': self.defaultCompany,
            'angelListLink': 'https://www.Angelist.com',
            'crunchbaseLink': 'https://www.crunchbase.com',
            'linkedInLink': 'https://www.linked-in.com',
            'classification': 'VC'
        }

    def test_update_investor_company_url(self):
        pass

    def test_get_update_investor_company_url(self):
        pass

    def test_get_update_investor_company_redirects_when_not_logged_in(self):
        pass

    def test_post_update_investor_company_redirects_when_not_logged_in(self):
        pass

    def test_successful_form(self):
        pass

    def test_unsuccessful_form(self):
        pass
