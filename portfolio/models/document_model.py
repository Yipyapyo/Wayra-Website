from django.db import models
from django.core.validators import RegexValidator
from portfolio.models import Company


class Document(models.Model):
    """A document stored in the system."""

    file_id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(
        max_length=254,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r"^[0-9a-zA-Z_\-. ]+$",
            message="Document name must consist of up to 254 valid characters: 0-9 a-z A-Z _ \\ - . and spaces"
        )]
    )
    file_type = models.CharField(
        max_length=254,
        unique=False,
        blank=False,
        validators=[RegexValidator(
            regex=r"^[0-9a-zA-Z_\-. ]+$",
            message="Document type must consist of up to 254 valid characters: 0-9 a-z A-Z _ \\ - . and spaces"
        )]
    )
    file_size = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to="documents/")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name
