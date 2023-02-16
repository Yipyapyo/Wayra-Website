"""Unit tests of the Programme model."""
from django.core.exceptions import ValidationError
from django.test import TestCase

from portfolio.models import Programme, Company, Portfolio_Company, Individual


class ProgrammeModelTestCase(TestCase):
    """Unit tests of the Programme model."""
    fixtures = ['portfolio/tests/fixtures/default_company.json',
                'portfolio/tests/fixtures/default_individual.json',
                'portfolio/tests/fixtures/default_portfolio_company.json',
                'portfolio/tests/fixtures/default_programme.json',
                ]

    def setUp(self) -> None:
        self.programme = Programme.objects.get(id=1)
        self.partner = Company.objects.get(id=1)
        self.participant = Portfolio_Company.objects.get(id=1)
        self.coach = Individual.objects.get(id=1)

        self.programme.partners.add(self.partner)
        self.programme.participants.add(self.participant)
        self.programme.coaches_mentors.add(self.coach)

    def _assert_programme_is_valid(self):
        try:
            self.programme.full_clean()
        except ValidationError:
            self.fail("Test programme should be valid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.programme.full_clean()

    def test_valid_programme(self):
        self._assert_programme_is_valid()
