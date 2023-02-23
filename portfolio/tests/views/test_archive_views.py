"""Unit tests of the archive views"""
from django.test import TestCase
from django.urls import reverse

from portfolio.models import User
from portfolio.tests.helpers import LogInTester, reverse_with_next


class ArchiveViewTestCase(TestCase):
    """Unit tests of the archive view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('archive_page')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")

    def test_archve_url(self):
        self.assertEqual(self.url, '/archive_page/')

    def test_get_archive(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/archive_page.html')

    def test_get_archive_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # def test_get_archive_redirects_when_not_admin(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     redirect_url = reverse('dashboard')
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)