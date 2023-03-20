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


class UploadDocumentViewsTestCase(TestCase):
    """Tests for the URLUploadForm."""

    fixtures = ["portfolio/tests/fixtures/default_company.json",
                'portfolio/tests/fixtures/default_user.json',
                ]


    def setUp(self):
        self.user = User.objects.get(email="john.doe@example.org")
        self.target_company = Company.objects.get(id=1)
        self.url = reverse('document_upload', kwargs={'company_id': self.target_company.id})
        self.form_data = {
            "file_name": "test_file.txt",
            "url": "https://www.wayra.uk",
            "is_private": True
        }
    
    def test_document_upload_url(self):
        self.assertEqual(self.url, f'/portfolio_company/{self.target_company.id}/upload_document/')

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

