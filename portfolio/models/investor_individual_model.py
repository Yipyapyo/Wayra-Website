"""The investor individual model."""
from django.db import models
from portfolio.models.individual_model import Individual, IndividualManager


class InvestorIndividual(Individual):
    """The investor individual model."""
    objects = IndividualManager()
    NumberOfPortfolioCompanies = models.PositiveIntegerField()
    NumberOfPersonalInvestments = models.PositiveIntegerField()
    NumberOfPartnerInvestments = models.PositiveIntegerField()
    PartOfIncubator = models.BooleanField()
    NumberOfExits = models.PositiveIntegerField()
