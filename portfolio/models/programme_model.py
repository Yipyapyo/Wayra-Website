from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from portfolio.models import Individual, Company, Portfolio_Company


class Programme(models.Model):
    """Model for programmes"""
    name = models.CharField(max_length=255)
    cohort = models.PositiveIntegerField(validators=[MinValueValidator(1, message="cohort has to be at least 1")])
    partners = models.ManyToManyField(Company, related_name="partners")
    participants = models.ManyToManyField(Portfolio_Company, related_name="participants")
    coaches_mentors = models.ManyToManyField(Individual)

    class Meta:
        unique_together = ('name', 'cohort')
