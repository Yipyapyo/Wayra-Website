from django.db import models
from portfolio.models.individual_model import Individual, IndividualManager
from portfolio.models.company_model import Company


class Founder(models.Model):
    """A founder of a company."""
    objects = IndividualManager()
    companyFounded = models.OneToOneField(Company, on_delete=models.CASCADE)
    individualFounder = models.OneToOneField(Individual, on_delete=models.CASCADE)



