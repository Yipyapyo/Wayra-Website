from django.db import models
from portfolio.models.investor_company_model import InvestorCompany
from portfolio.models.company_model import PortfolioCompany
from django.core.validators import MaxValueValidator
from django.utils import timezone
from portfolio.models.investor_individual_model import InvestorIndividual

FOUNDING_ROUNDS = [
    ('Seed round', 'Seed round'),
    ('Series A', 'Series A'),
    ('Series B', 'Series B'),
    ('Series C', 'Series C'),
    ('Coporate round', 'Coporate round'),
    ('Convertible note', 'Convertible note'),
    ('Venture round', 'Venture round'),
    ('Debt financing', 'Debt financing'),
    ('Post-IPO Equity', 'Post-IPO Equity')
]


class Investment(models.Model):
    """Investment model for a investment from an investor to a startups"""
    investor = models.ManyToManyField(InvestorCompany, related_name="investor")
    individualInvestor = models.ManyToManyField(InvestorIndividual, related_name="IndividualInvestor")
    startup = models.ManyToManyField(PortfolioCompany, related_name="startup")
    typeOfFoundingRounds = models.CharField(max_length=50, choices=FOUNDING_ROUNDS)
    moneyRaised = models.DecimalField("In millions", max_digits=5, decimal_places=2)
    dateInvested = models.DateTimeField(auto_now=True, validators=[MaxValueValidator(limit_value=timezone.now)])

