from django.db import models
from portfolio.models.individual_model import Individual, IndividualManager


class InvestorIndividual(Individual):
    """An investor in a company."""
    objects = IndividualManager()

    NumberOfPortfolioCompanies = models.PositiveIntegerField()
    NumberOfPersonalInvestments = models.PositiveIntegerField()
    NumberOfPartnerInvestments = models.PositiveIntegerField()
    PartOfIncubator = models.BooleanField()
    NumberOfExits = models.PositiveIntegerField()
