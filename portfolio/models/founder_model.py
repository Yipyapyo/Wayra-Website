from django.db import models
from portfolio.models.individual_model import Individual
from portfolio.models.company_model import Company

class Founder(Individual):
    company = models.ManyToManyField(Company, related_name="companies")
    additionalInformation = models.CharField(max_length=500, blank=True)

