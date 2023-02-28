from django.db import models
from portfolio.models.individual_model import Individual


class InvestorIndividual(Individual):
    """An investor in a company."""

    NumberOfPortfolioCompanies = models.PositiveIntegerField()
    NumberOfPersonalInvestments = models.PositiveIntegerField()
    NumberOfPartnerInvestments = models.PositiveIntegerField()
    PartOfIncubator = models.BooleanField(blank=False)
    NumberOfExits = models.PositiveIntegerField()
