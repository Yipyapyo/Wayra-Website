from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

# Create your models here.
class individual_create(models.Model):
    """Individual model used by admins to create new client/individual."""
    AngelListLink = models.URLField("Angellist link", max_length = 200)
    CrunchbaseLink = models.URLField("Crunchbase link", max_length = 200)
    LinkedInLink = models.URLField("Linkedin link", max_length = 200)
    Company = models.CharField("Company", max_length = 100)
    Position = models.CharField("Company position", max_length = 100)
    Email = models.EmailField(blank = False)
    PrimaryNumber = PhoneNumberField("Primary phone number", blank = False)
    SecondaryNumber = PhoneNumberField("Secondary phone number", blank = True)

class residentialAddress(models.Model):
    """Model to store addresses for individuals"""
    address_line1 = models.CharField("Address line 1", max_length = 50, blank=False)
    address_line2 = models.CharField("Address line 2", max_length = 50, blank=True)
    postal_code = models.CharField("Postal code", max_length = 10)
    city = models.CharField("City", max_length=50, blank=False)
    state = models.CharField("State/Province", max_length=50, blank=True)
    country = CountryField(blank_label="Select country")
    individual = models.ForeignKey(individual_create, on_delete=models.CASCADE)

