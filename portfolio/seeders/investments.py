import random

from django.core.exceptions import ObjectDoesNotExist

from portfolio.seeders import Seeder
from portfolio.models import InvestorCompany, Company, Investment, Portfolio_Company
from portfolio.models.investment_model import FOUNDING_ROUNDS


class InvestorCompanySeeder(Seeder):
    INVESTOR_COMPANY_COUNT = 5

    def seed(self):
        self._create_investor_companies(self.INVESTOR_COMPANY_COUNT)
        print(f"{InvestorCompany.objects.count()} investor companies in the db.\n")

    def _create_investor_companies(self, count):
        for i in range(1, count + 1):
            try:
                InvestorCompany.objects.get(id=i)
                print(f"InvestorCompany with id({i}) has already seeded.")
            except ObjectDoesNotExist:
                InvestorCompany.objects.create(
                    company=Company.objects.get(id=i),
                    angelListLink="https://www.Angelist.com",
                    crunchbaseLink="https://www.crunchbase.com/",
                    linkedInLink="https://www.linkedin.com/",
                    classification=InvestorCompany.INVESTOR_TYPES[i],
                )
                print(f"InvestorCompany with id({i}) has been seeded.")


class InvestmentSeeder(Seeder):
    INVESTMENT_COUNT = 25

    def seed(self):
        self._create_investments(self.INVESTMENT_COUNT)
        print(f"{Investment.objects.count()} investments in the db.\n")

    def _get_objects_from_models(self, model, index, slice_size):
        random_number_of_object = random.randint(1, slice_size)
        objects = list(
            model.objects.filter(id__in=range(index * slice_size, index * slice_size + random_number_of_object)))
        return objects

    def _create_investments(self, count):
        company_count = 1
        for i in range(1, count + 1):
            try:
                Investment.objects.get(id=i)
                print(f"InvestorCompany with id({i}) has already seeded.")
            except ObjectDoesNotExist:
                Investment.objects.create(
                    investor=InvestorCompany.objects.get(id=company_count),
                    startup=Portfolio_Company.objects.get(wayra_number=f'WN-{i}'),
                    typeOfFoundingRounds=random.choice(FOUNDING_ROUNDS)[1],
                    investmentAmount=random.randint(10_000, 10_000_000),
                    dateInvested=self.faker.date_this_century(),
                )
                if random.randint(0, 101) > 30 and company_count != 5:
                    company_count += 1

                print(f"Investment with id({i}) has been seeded.")
