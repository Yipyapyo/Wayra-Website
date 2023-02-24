"""Unit tests of the settings views"""
from django.test import TestCase
from django.urls import reverse
from portfolio.models import User
from portfolio.tests.helpers import LogInTester, reverse_with_next
from portfolio.forms import ChangePasswordForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse


class SettingsViewTestCase(TestCase, LogInTester):
    """Unit tests of the dashboard view"""
    fixtures = [
        "portfolio/tests/fixtures/default_user.json",
    ]

    def setUp(self) -> None:
        self.url = reverse('account_settings')
        self.change_password_url = reverse('change_password')
        self.user = User.objects.get(email="john.doe@example.org")
        self.form_input = {
             "old_password" : "Password123",
             "new_password" : "Password321",
             "confirm_password" : "Password321",
        }

    def test_account_settings_url(self):
        self.assertEqual(self.url, '/account_settings/')

    def test_change_password_url(self):
        self.assertEqual(self.change_password_url, '/account_settings/change_password')

    def test_get_account_settings(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings/account_settings.html')

    def test_get_account_settings_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_account_settings_uses_the_correct_templates(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings/change_password_section.html')
        self.assertTemplateUsed(response, 'settings/contact_details_section.html')
        self.assertTemplateUsed(response, 'settings/deactivate_account.html')
        self.assertTemplateUsed(response, 'settings/links_section.html')
        self.assertTemplateUsed(response, 'settings/upload_profile_section.html')

    def test_get_account_settings_parses_the_correct_form(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(isinstance(form, ChangePasswordForm))
        self.assertFalse(form.is_bound)

    #Change password Tests
    def test_password_changed_successful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ChangePasswordForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertTrue(check_password(self.form_input["old_password"], self.user.password))

        response = self.client.post(self.change_password_url, self.form_input, follow=True)
        user = User.objects.get(email=self.user.email)
        self.assertTrue(user)
        response_url = reverse('account_settings')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTrue(check_password(self.form_input["new_password"], user.password))

    def test_password_changed_unsuccessful(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.change_password_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

        form = ChangePasswordForm(data=self.form_input, user=self.user)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertTrue(check_password(self.form_input["old_password"], self.user.password))

        self.form_input["confirm_password"] = "WrongPassword"

        response = self.client.post(self.change_password_url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_password(self.form_input["old_password"], self.user.password))
        self.assertFalse(check_password(self.form_input["new_password"], self.user.password))
        form=response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['confirm_password'][0], 'Confirmation does not match password.')
