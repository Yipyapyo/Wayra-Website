from django.db import models
from portfolio.models.individual_model import Individual

class InvestorIndividual(Individual):
    NumberOfPortfolioCompanies = models.PositiveIntegerField()
    NumberOfPersonalInvestments = models.PositiveIntegerField()
    NumberOfPartnerInvestments = models.PositiveIntegerField()
    PartOfIncubator = models.BooleanField(blank=False)
    NumberOfExits = models.PositiveIntegerField()