from django.db import models
from django.dispatch import receiver
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
        """Define a constraint to ensure both the url and file fields are not null at the same time."""

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_url_or_file",
                check=(
                    models.Q(url__isnull=True, file__gt="") | models.Q(url__isnull=False, file__exact="")
                ),
            )
        ]


@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes the file from local storage when the corresponding "Document" object is deleted."""

    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes the old file from local storage when corresponding "Document" object is updated with a new file."""

    if not instance.pk:
        return False

    try:
        old_file = Document.objects.get(pk=instance.pk).file
    except Document.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file and old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)