from django.db import models
from portfolio.models import Individual, Company, Portfolio_Company

class Programme(models.Model):
    """Model for programmes"""
    name = models.CharField(max_length=255)
    cohort = models.PositiveIntegerField()
    partners = models.ManyToManyField(Company, related_name="partners")
    participants = models.ManyToManyField(Portfolio_Company, related_name="participants")
    coaches_mentors = models.ManyToManyField(Individual)
    
