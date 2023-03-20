import mimetypes
import os
import shutil
import time
from io import BytesIO
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.db import IntegrityError
from django.test import TestCase
from portfolio.models import Company, Document, User
from portfolio.forms import URLUploadForm, DocumentUploadForm
from vcpms.settings import MEDIA_ROOT
from portfolio.tests.helpers import LogInTester, reverse_with_next


class DocumentViewsTestCase(TestCase):
    """Tests for the URLUploadForm."""

    fixtures = ["portfolio/tests/fixtures/default_company.json",
                'portfolio/tests/fixtures/default_user.json',
                ]


    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.defaultCompany = Company.objects.get(id=1)
        self.url = reverse('document_upload', kwargs={'company_id': self.defaultCompany.id})
        self.url_form_data = {
            "upload_url" : 'True',
            "file_name": "test_file.txt",
            "url": "https://www.wayra.uk",
            "is_private": True
        }
        file = BytesIO()
        file.write(open("portfolio/tests/forms/TestingExcel.xlsx", 'rb').read())
        file.seek(0)

        self.defaultCompany = Company.objects.get(id=1)
        self.file_data = SimpleUploadedFile("TestingExcel.xlsx", file.read(), content_type=mimetypes.guess_type(
            "portfolio/tests/forms/TestingExcel.xlsx"))
        self.document_form_input = {
            "upload_file" : 'True',
            "file": self.file_data,
            "is_private": True
            }
        directory = os.path.join(MEDIA_ROOT, f'documents/{self.defaultCompany.name}')
        directory = os.path.normpath(directory)
        for i in range(10):
            # Multi-threaded test causes locking
            try:
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
            except IOError:
                time.sleep(.1)
        

    
    def test_document_upload_url(self):
        self.assertEqual(self.url, f'/portfolio_company/{self.defaultCompany.id}/upload_document/')

    def test_get_document_upload_view(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'document/document_upload.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, DocumentUploadForm))
        self.assertFalse(form.is_bound)

    def test_document_upload_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_upload_url(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Document.objects.count()
        response = self.client.post(self.url, self.url_form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Document.objects.count()
        self.assertEqual(before_count, after_count-1)
    
    def test_post_upload_document(self):
        self.client.login(email=self.user.email, password="Password123")
        before_count = Document.objects.count()
        response = self.client.post(self.url, self.document_form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = Document.objects.count()
        self.assertEqual(before_count, after_count-1)

    # def test_download_document(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     document = Document.objects.get(id=1)
    #     self.url = reverse('download_document', kwargs={'file_id': Document.id})
    #     response = self.client.get()
    
    # def test_delete_document_url(self):
        # self.assertEqual(self.url, f'/programme_page/{self.target_programme.id}/delete/')

    # def test_delete_document(self):

    # # def test_document_delete_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('login', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # def test_document_change_permissions(self):