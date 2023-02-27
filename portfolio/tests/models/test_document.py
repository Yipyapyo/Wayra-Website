from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Document
from portfolio.models import Company


class DocumentModelTestCase(TestCase):
    """Unit tests for the Document model."""

    fixtures = ["portfolio/tests/fixtures/default_company.json"]

    def setUp(self):
        self.document = Document.objects.create(
            file_name="test",
            file_type="document",
            company=Company.objects.get(id=1),
            file=SimpleUploadedFile("test.document", b"file contents")
        )

    def test_valid_document(self):
        self._assert_document_is_valid()

    """Helper functions"""

    # Assert a document is valid
    def _assert_document_is_valid(self):
        try:
            self.document.full_clean()
        except ValidationError:
            self.fail("Test document is not valid.")

    # Assert a document is invalid
    def _assert_document_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.document.full_clean()

    # Create a second document
    def _create_second_document(self):
        document = Document.objects.create(
            file_name="test2",
            file_type="document",
            company=Company.objects.get(id=1),
            file=SimpleUploadedFile("test2.document", b"file contents")
        )
        return document
