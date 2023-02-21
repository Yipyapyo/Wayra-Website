from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

class Company(models.Model):
    """A company to store information about."""

    name = models.CharField(
        max_length=60,
        unique=True,
        blank=False,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    company_registration_number = models.CharField('Company Registration Number',default="00000000", blank=False, max_length=8, 
                              validators=[MinLengthValidator(8)])
    trading_names = models.CharField(
        max_length=60,
        unique=True,
        blank=True,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    previous_names = models.CharField(
        max_length=60,
        unique=True,
        blank=True,
        validators=[RegexValidator(
            regex=r"^[a-zA-Z0-9 ,]{3,}$",
            message="Company name must consist of three to sixty characters"
        )]
    )
    registered_address = models.CharField("Registered Address", max_length = 50, blank=True) #models.ForeignKey(ResidentialAddress, on_delete=models.CASCADE, null=True)
    jurisdiction = models.CharField("Jurisdiction", max_length = 50, blank=True)
    founders = None     # models.ForeignKey(Individual)
    incorporation_date = models.DateField(auto_now=True)
    investors = None    # e.g. models.ForeignKey(Individual)
    programmes = None  # e.g. models.ForeignKey(Programme)
    mentors = None # e.g. models.ForeignKey(Mentor)
    coaches = None # e.g. models.ForeignKey(Coach)

class Portfolio_Company(Company):
    wayra_number = models.CharField(max_length=255)


