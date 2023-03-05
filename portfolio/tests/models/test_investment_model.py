from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from portfolio.models import Company, Portfolio_Company, Investment, InvestorCompany


class InvestmentModelTestCase(TestCase):
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
        self.portfolio_company = Portfolio_Company.objects.get(id=1)
        self.investment = Investment.objects.create(
            investor=self.investorCompany,
            startup=self.portfolio_company,
            typeOfFoundingRounds='Series A',
            dateInvested=timezone.now().date(),
            dateExit=None,
            contractRight="Template - Contract - Right"
        )

    def _assert_valid_investment(self):
        try:
            self.investment.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_invalid_investment(self):
        with self.assertRaises(ValidationError):
            self.investment.full_clean()

    def test_valid_investment(self):
        self._assert_valid_investment()

    def test_investment_amount_cannot_exceed_15_digits(self):
        pass

    def test_investment_amount_cannot_exceed_2_dp(self):
        pass

    def test_investment_amount_can_be_15_digits(self):
        pass

    def test_investment_can_hv_two_dp(self):
        pass

    def test_investment_cannot_be_negative(self):
        pass

    def test_date_invested_can_be_today(self):
        pass

    def test_date_invested_cannot_be_tomorrow(self):
        pass

    def test_date_invested_cannot_be_blank(self):
        pass

    def test_date_invested_cannot_be_after_date_exit(self):
        pass

    def test_date_exit_can_be_blank(self):
        pass

    def test_date_exit_can_be_after_date_invested(self):
        pass

    def test_date_exit_cannot_be_before_date_invested(self):
        pass

    def test_contractRight_cannot_be_blank(self):
        pass

    def test_contractRight_can_be_1000_characters(self):
        pass

    def test_contractRight_cannot_be_over_1000_characters(self):
        pass

    def test_investor_cannot_be_blank(self):
        pass

    def test_investor_delete_deletes_investment(self):
        pass

    def test_startup_cannot_be_blank(self):
        pass

    def test_startup_delete_deletes_investment(self):
        pass

class InvestorCompanyModelTestCase(TestCase):
    fixtures = ['portfolio/tests/fixtures/default_company.json']
    def setUp(self) -> None:
        self.defaultCompany = Company.objects.get(id=1)
        self.investorCompany = InvestorCompany.objects.create(
            company=self.defaultCompany,
            angelListLink='https://www.Angelist.com',
            crunchbaseLink='https://www.crunchbase.com',
            linkedInLink='https://www.linked-in.com',
            classification='VC'
        )
    def _assert_valid_investment(self):
        try:
            self.investorCompany.full_clean()
        except ValidationError:
            self.fail("Test user should be valid")

    def _assert_invalid_investment(self):
        with self.assertRaises(ValidationError):
            self.investorCompany.full_clean()

    def test_angellistlink_can_be_200_characters_long(self):
        pass

    def test_angellistlink_cannot_be_over_200_characters_long(self):
        pass

    def test_crunchbaselink_cannot_be_blank(self):
        pass

    def test_crunchbaselink_can_be_200_characters_long(self):
        pass

    def test_crunchbaselink_cannot_be_over_200_characters_long(self):
        pass

    def test_linkedinlink_cannot_be_blank(self):
        pass

    def test_linkedinlink_can_be_200_characters_long(self):
        pass

    def test_linkedinlink_cannot_be_over_200_characters_long(self):
        pass

    def test_company_cannot_be_blank(self):
        pass

    def test_delete_company_deletes_investor_company(self):
        pass

    def test_classification_cannot_be_none(self):
        pass