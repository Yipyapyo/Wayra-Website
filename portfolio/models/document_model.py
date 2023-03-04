from django.db import models
from django.core.validators import RegexValidator
from portfolio.models import Company
import os


DEFAULT_PATH = "documents/"


# Returns the storage path of a file.
def get_path(instance, file_name):
    return os.path.join(DEFAULT_PATH, instance.company.name, file_name)


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
    url = models.URLField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to=get_path, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        """Define a constraint to ensure either an url or file is not null."""

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_url_or_file",
                check=(
                    models.Q(url__isnull=True, file__isnull=False) | models.Q(url__isnull=False, file__isnull=True)
                ),
            )
        ]
