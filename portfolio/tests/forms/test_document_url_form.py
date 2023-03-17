from django.test import TestCase
from portfolio.models import Company
from portfolio.forms import URLUploadForm


class URLUploadFormTest(TestCase):
    """Tests for the URLUploadForm."""

    fixtures = ["portfolio/tests/fixtures/default_company.json"]

    def setUp(self):
        self.form_data = {
            "file_name": "test_file.txt",
            "url": "https://www.wayra.uk",
            "is_private": True
        }

    def test_form_is_valid(self):
        form = URLUploadForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        document = form.save(commit=False)
        document.company = Company.objects.get(id=1)
        document.save()
        self.assertEqual(document.file_name, self.form_data["file_name"])
        self.assertEqual(document.file_type, "URL")
        self.assertEqual(document.url, self.form_data["url"])
        self.assertTrue(document.is_private)

    def test_form_is_invalid(self):
        form_data = {
            "file_name": None,
            "url": None,
            "is_private": True
        }
        form = URLUploadForm(data=form_data)
        self.assertFalse(form.is_valid())
