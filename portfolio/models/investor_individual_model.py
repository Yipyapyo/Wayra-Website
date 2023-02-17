from django.db import models
from individual_model import Individual

class InvestorIndividual(Individual):

    NumberOfPortfolioCompanies = models.PositiveIntegerField()
    NumberOfPersonalInvestments = models.PositiveIntegerField()
    NumberOfPartnerInvestments = models.PositiveIntegerField()
    NumberOfExits = models.PositiveIntegerField()