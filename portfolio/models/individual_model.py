from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Individual(models.Model):
    """Individual model used by admins to create new client/individual."""
    AngelListLink = models.URLField("Angellist link", max_length=200)
    CrunchbaseLink = models.URLField("Crunchbase link", max_length=200)
    LinkedInLink = models.URLField("Linkedin link", max_length=200)
    Company = models.CharField("Company", max_length=100)
    Position = models.CharField("Company position", max_length=100)
    Email = models.EmailField(blank=False)
    PrimaryNumber = PhoneNumberField("Primary phone number", blank=False)
    SecondaryNumber = PhoneNumberField("Secondary phone number", blank=True)
