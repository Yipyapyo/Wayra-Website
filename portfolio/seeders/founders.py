from portfolio.seeders import Seeder
from portfolio.models import Founder, Company, Individual
import random


class FounderSeeder(Seeder):
    FOUNDER_COUNT = 10

    def seed(self):
        self._populate_founders(self.FOUNDER_COUNT)
        print(f"{Founder.objects.count()} founders in the db.\n")


    def _populate_founders(self, count):
        """Seeder for fake founders"""
        print('seeding founders...')
        for i in range(1,count+1):

            founder = Founder.objects.create(
                companyFounded=Company.objects.get(id=i),
                individualFounder=Individual.objects.get(id=i),
            )
            founder.save()
            print(F"Founders with id({founder.id}) has been seeded.")
