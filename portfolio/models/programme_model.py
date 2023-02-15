from django.db import models
from portfolio.models import Individual, Company, Portfolio_Company

class Programme(models.model):
    """Model for programmes"""
    name = models.CharField(max_length=255)
    cohort = models.PositiveIntegerField()
    partners = models.ManyToManyField(Company)
    participants = models.ManyToManyField(Portfolio_Company)
    coaches_mentors = models.ManyToManyField(Individual)
    
