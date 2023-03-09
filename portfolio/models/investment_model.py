from django.db import models
from portfolio.models import Portfolio_Company, Company, Individual
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

class Investor(models.Model):
    VENTURE_CAPITAL = 'VC'
    PRIVATE_EQUITY_FIRM = 'PEF'
    ACCELERATOR = 'A'
    INVESTMENT_PARTNER = 'IP'
    CORPORATE_VENTURE_CAPITAL = 'CVC'
    MICRO_VC = 'MVC'
    ANGEL_GROUP = 'AG'
    INCUBATOR = 'I'
    INVESTMENT_BANK = 'IB'
    FAMILY_INVESTMENT_OFFICE = 'FIO'
    VENTURE_DEBT = 'VD'
    CO_WORKING_SPACE = 'CWS'
    FUND_OF_FUNDS = 'FOF'
    HEDGE_FUND = 'HF'
    GOVERNMENT_OFFICE = 'GO'
    UNIVERSITY_PROGRAM = 'UP'
    ENTREPRENEURSHIP_PROGRAM = 'EP'
    SECONDARY_PURCHASER = 'SP'
    STARTUP_COMPETITION = 'SC'
    SYNDICATE = 'S'
    PENSION_FUNDS = 'PF'

    INVESTOR_TYPES = [
        ('VENTURE_CAPITAL', 'Venture Capital'),
        ('PRIVATE_EQUITY_FIRM', 'Private Equity Firm'),
        ('ACCELERATOR', 'Accelerator'),
        ('INVESTMENT_PARTNER', 'Investment Partner'),
        ('CORPORATE_VENTURE_CAPITAL', 'Corporate Venture Capital'),
        ('MICRO_VC', 'Micro VC'),
        ('ANGEL_GROUP', 'Angel Group'),
        ('INCUBATOR', 'Incubator'),
        ('INVESTMENT_BANK', 'Investment Bank'),
        ('FAMILY_INVESTMENT_OFFICE', 'Family Investment Office'),
        ('VENTURE_DEBT', 'Venture Debt'),
        ('CO_WORKING_SPACE', 'Co-Working Space'),
        ('FUND_OF_FUNDS', 'Fund Of Funds'),
        ('HEDGE_FUND', 'Hedge Fund'),
        ('GOVERNMENT_OFFICE', 'Government Office'),
        ('UNIVERSITY_PROGRAM', 'University Program'),
        ('ENTREPRENEURSHIP_PROGRAM', 'Entrepreneurship Program'),
        ('SECONDARY_PURCHASER', 'Secondary Purchaser'),
        ('STARTUP_COMPETITION', 'Startup Competition'),
        ('SYNDICATE', 'Syndicate'),
        ('PENSION_FUNDS', ' Pension Funds'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null = True, blank = True, related_name = "company")
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, null = True, blank = True, related_name = "individual")
    classification = models.CharField(
        max_length=50,
        choices=INVESTOR_TYPES,
        default=VENTURE_CAPITAL,
    )

class Investment(models.Model):
    """Investment model for a investment from an investor to a startups"""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="investor")
    startup = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="startup")
    typeOfFoundingRounds = models.CharField(max_length=50, choices=FOUNDING_ROUNDS)
    investmentAmount = models.DecimalField(max_digits=15, decimal_places=2)
    dateInvested = models.DateField(validators=[MaxValueValidator(limit_value=timezone.now().date())])
    dateExit = models.DateField(blank=True, null=True)



class ContractRight(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    right = models.CharField(max_length = 255)
    details = models.CharField(max_length = 255)


