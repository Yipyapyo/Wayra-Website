"""Unit tests of the log in view"""

from django.test import TestCase
from django.urls import reverse
from django.contrib import messages

from portfolio.forms import LogInForm
from portfolio.models import User
from portfolio.tests.helpers import LogInTester


class LogInViewTestCase(TestCase, LogInTester):
    """Unit tests of the log in view"""

    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
        "portfolio/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.get(email="john.doe@example.org")
        self.admin_user = User.objects.get(email="petra.pickles@example.org")

    def test_log_in_url(self):
        self.assertEqual(self.url, '/login')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_user_log_in(self):
        form_input = {'email': "john.doe@example.org", 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_user_log_in(self):
        form_input = {'email': 'john.doe@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_successful_admin_log_in(self):
        form_input = {'email': 'petra.pickles@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'email': 'john.doe@example.org', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_get_login_redirects_when_user_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_post_login_redirects_when_user_logged_in(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        form_input = {"email": "wrong.user@example.org", "password": "WrongPassword"}
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_get_login_redirects_when_admin_logged_in(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_post_login_redirects_when_admin_logged_in(self):
        self.client.login(email=self.admin_user.email, password="Password123")
        form_input = {"email": "wrong.user@example.org", "password": "WrongPassword"}
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "dashboard.html")