from django.core.exceptions import ValidationError
from django.db import models

from portfolio.models import Company
from portfolio.models.investor_model import Investor


class Portfolio_Company(models.Model):
    parent_company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="parent_company")
    wayra_number = models.CharField(max_length=255, unique=True)

    def clean(self):
        if Investor.objects.filter(company=self.parent_company).count() > 0:
            raise ValidationError('Company selected cannot be a Investor Company')
