from django.core.management import BaseCommand

from portfolio.seeders import *


class Command(BaseCommand):
    seeders = [UserSeeder(),
               CompanySeeder(),
               PortfolioCompaniesSeeder(),
               IndividualSeeder(),
               InvestorCompanySeeder(),
               InvestmentSeeder(),
               ProgrammeSeeder(),
               ]

    def handle(self, *args, **options):
        print("seeding...")
        for seeder in self.seeders:
            seeder.seed()
        print(f"done.")

