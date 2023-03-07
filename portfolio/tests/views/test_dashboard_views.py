"""Unit tests of the dashboard views"""
from django.test import TestCase
from django.urls import reverse

from portfolio.models import User
from portfolio.tests.helpers import LogInTester, reverse_with_next

from portfolio.tests.helpers import set_session_variables

class DashboardViewTestCase(TestCase, LogInTester):
    """Unit tests of the dashboard view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('dashboard')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")
        set_session_variables(self.client)

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard')

    def test_get_dashboard(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/main_dashboard.html')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
