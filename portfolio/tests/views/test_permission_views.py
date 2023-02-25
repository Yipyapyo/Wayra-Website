""" Unit test for permission views"""
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from portfolio.forms import UserCreationForm
from portfolio.models import User, Company
from portfolio.tests.helpers import reverse_with_next
from vcpms import settings


class UserListViewTestCase(TestCase):
    """ Unit test for user list """
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('permission_user_list')
        self.user = User.objects.get(email='petra.pickles@example.org')

    def test_user_list_url(self):
        self.assertEqual(self.url, '/permissions/users/')

    def test_get_user_list(self):
        self.client.login(username=self.user.email, password="Password123")
        self._create_test_users(15 - 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15 - 1):
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'+447312345678')
            self.assertIsNotNone(User.objects.get(email=f'user{user_id}@test.org'))

    def test_user_list_pagination(self):
        self.client.login(email=self.user.email, password="Password123")
        # minus John doe
        self._create_test_users(settings.ADMINS_USERS_PER_PAGE * 2 + 1 - 1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')

        page_obj = response.context['page_obj']
        page_one_url = reverse('permission_user_list') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')
        self.assertEqual(len(response.context['users']), settings.ADMINS_USERS_PER_PAGE)
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('permission_user_list') + '?page=2'
        response = self.client.get(page_two_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')
        self.assertEqual(len(response.context['users']), settings.ADMINS_USERS_PER_PAGE)
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('permission_user_list') + '?page=3'
        response = self.client.get(page_three_url)
        page_obj = response.context['page_obj']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')
        self.assertEqual(len(response.context['users']), 1)
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    def test_non_admin_cannot_access_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(email=f'user{user_id}@test.org',
                                     password='Password123',
                                     first_name=f'First{user_id}',
                                     last_name=f'Last{user_id}',
                                     phone=f'+447312345678'
                                     )


class UserSignUpFormViewTestCase(TestCase):
    """ Unit test for UserSignUpFormView"""
    fixtures = ['portfolio/tests/fixtures/default_user.json',
                'portfolio/tests/fixtures/other_users.json']

    def setUp(self) -> None:
        self.url = reverse('permission_create_user')
        self.grp = Group.objects.create(name="DefaultGrp")
        content_type = ContentType.objects.get_for_model(Company)
        for permission in list(Permission.objects.filter(content_type=content_type)):
            self.grp.permissions.add(permission)
        self.form_input = {"email": "jane.doe@example.org",
                           "first_name": "Jane",
                           "last_name": "Doe",
                           "phone": "+447312345678",
                           "password": 'Password123',
                           "is_active": True,
                           "group": [1],
                           }

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/permissions/create_user/')

    def test_non_admin_cannot_get_page(self):
        redirect_url = reverse('dashboard')
        self.client.login(username='john.doe@example.org', password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', reverse('dashboard'))
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_user_sign_up(self):
        before_count = User.objects.count()
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('permission_user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'permissions/permission_list_page.html')
        user = User.objects.get(email='jane.doe@example.org')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        is_password_equal = check_password('Password123', user.password)
        self.assertTrue(is_password_equal)
        self.assertEqual(user.phone, "+447312345678")
        self.assertEqual(user.is_active, True)
        self.assertEqual(list(user.groups.all()), [self.grp])

    def test_unsuccessful_user_sign_up(self):
        before_count = User.objects.count()
        self.form_input["email"] = "INVALID_EMAIL"
        self.client.login(username='petra.pickles@example.org', password="Password123")
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'permissions/user_create.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserCreationForm))
        self.assertTrue(form.is_bound)


class GroupCreationViewTestCase(TestCase):
    """ Unit test for GroupCreationView"""
    pass


class UserDeleteViewTestCase(TestCase):
    """ Unit test for UserDeleteView"""
    pass
