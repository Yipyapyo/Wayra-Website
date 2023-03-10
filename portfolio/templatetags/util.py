from django import template
from portfolio.models import Founder, Individual
from portfolio.models.investor_individual_model import InvestorIndividual

register = template.Library()

@register.filter
def is_investor(value):
    if isinstance(value, InvestorIndividual):
        return True

@register.filter
def is_founder(value):
    if isinstance(value, Founder):
        return True

