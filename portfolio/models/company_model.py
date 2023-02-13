from django.db import models
from django.core.validators import RegexValidator


class Company(models.Model):
    """A company to store information about."""

    name = models.CharField(
        max_length=60,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ]*$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    founders = None     # models.ForeignKey(Individual)
    incorporation_date = models.DateField(auto_now=True)
    investors = None    # e.g. models.ForeignKey(Individual)
