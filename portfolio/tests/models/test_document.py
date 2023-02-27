from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Document


class DocumentModelTestCase(TestCase):
    """Unit tests for the Document model."""

    def setUp(self):
        self.document = Document.objects.create(
            name="test.document",
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
            name="test-2.document",
            file=SimpleUploadedFile("test-2.document", b"file contents")
        )
        return document
