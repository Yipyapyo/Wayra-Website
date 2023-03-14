from django import forms
from portfolio.models import Document


class DocumentForm(forms.ModelForm):
    """Form for storing a document."""

    class Meta:
        model = Document
        fields = ["file_name", "file_type", "file_size", "url", "file", "company"]
