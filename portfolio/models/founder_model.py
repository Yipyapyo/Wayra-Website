from django.db import models
from portfolio.models.individual_model import Individual
# from portfolio.models.company_model import Company


class Founder(Individual):
    """A founder of a company."""
    companyFounded = models.CharField(max_length=100, blank=False, default="startup")
    additionalInformation = models.CharField(max_length=500, blank=True)
