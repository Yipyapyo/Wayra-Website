from django.db import models
from founder_model import Founder

class pastExperience(models.model):
    individual = models.ForeignKey(Founder, on_delete=models.CASCADE)
    companyName = models.CharField(max_length = 100)
    workTitle = models.CharField(max_length = 100)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(blank=True)
    duration = models.CharField(max_length = 50, default="present")
    Description = models.CharField(max_length = 500, blank=True)

