from django.db import models
from portfolio.models import InvestorCompany, Portfolio_Company
from django.core.validators import MaxValueValidator
from django.utils import timezone

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
    investor = models.ForeignKey(InvestorCompany, on_delete=models.CASCADE, related_name="investor")
    startup = models.ForeignKey(Portfolio_Company, on_delete=models.CASCADE, related_name="startup")
    typeOfFoundingRounds = models.CharField(max_length=50, choices=FOUNDING_ROUNDS)
    investmentAmount = models.DecimalField(max_digits=15, decimal_places=2)
    dateInvested = models.DateTimeField(auto_now=True, validators=[MaxValueValidator(limit_value=timezone.now)])
    dateExit = models.DateTimeField(blank=True, null=True)

