from django.db import models


class Document(models.Model):
    """A document stored in the system."""

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents")
