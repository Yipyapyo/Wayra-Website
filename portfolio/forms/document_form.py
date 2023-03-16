from django import forms
from portfolio.models import Document, Company
from django.utils.translation import gettext_lazy as _


class DocumentUploadForm(forms.ModelForm):
    """A form for storing a document."""

    class Meta:
        model = Document
        fields = ["file"]
        exclude = ["file_name", "file_type", "file_size", "url", "company", "created_at", "updated_at"]
        labels = {
            "file": _("Select a file to upload:")
        }

    def save(self, commit=True):
        document = super().save(commit=False)
        document.file_name = self.cleaned_data["file"].name
        document.file_type = self.cleaned_data["file"].name.split(".")[-1]
        document.file_size = self.cleaned_data["file"].size

        if commit:
            document.save()

        return document


class URLUploadForm(forms.ModelForm):
    """A form for storing an URL."""

    class Meta:
        model = Document
        fields = ["file_name", "url"]
        exclude = ["file_type", "file_size", "file", "company", "created_at", "updated_at"]
        labels = {
            "file_name": _("File name:"),
            "url": _("URL:")
        }

    def save(self, commit=True):
        document = super().save(commit=False)
        document.file_name = self.cleaned_data["file_name"]
        document.file_type = "URL"

        if commit:
            document.save()

        return document
