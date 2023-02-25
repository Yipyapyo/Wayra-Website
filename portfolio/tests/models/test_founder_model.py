from django.test import TestCase
from portfolio.models import Founder
from phonenumber_field.phonenumber import PhoneNumber
from django.core.exceptions import ValidationError

class FounderModelTestCase(TestCase):
    """Unit test for the founder model."""
    def setUp(self):
        self.founder = Founder.objects.create(
            name="ben",
            AngelListLink="https://www.AngelList.com",
            CrunchbaseLink="https://www.Crunchbase.com",
            LinkedInLink="https://www.LinkedIn.com",
            Company="exampleCompany",
            Position="examplePosition",
            Email="test@gmail.com",
            PrimaryNumber=PhoneNumber.from_string("+447975777666"),
            SecondaryNumber=PhoneNumber.from_string("+441325777655"),
            companyFounded="Startup",
            additionalInformation="Founder of the startup company.",
        )
    
    def test_valid_founder(self):
        self._assert_founder_is_valid()

    def test_company_founded_cannot_be_blank(self):
        self.founder.companyFounded = ""
        self._assert_founder_is_invalid()
    
    def test_company_founded_maximum_length_100(self):
        self.founder.companyFounded = ("x" * 101)
        self._assert_founder_is_invalid()
    
    def test_additionalInformation_can_be_blank(self):
        self.founder.additionalInformation = ""
        self._assert_founder_is_valid()

    def _assert_founder_is_valid(self):
        try:
            self.founder.full_clean()
        except ValidationError:
            self.fail('Test founder is not valid.')

    # Assert a individual is invalid
    def _assert_founder_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.founder.full_clean()

