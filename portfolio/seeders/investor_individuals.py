from portfolio.seeders import Seeder
from portfolio.models import InvestorIndividual, ResidentialAddress
import random


class InvestorIndividualSeeder(Seeder):
    INVESTOR_COUNT = 10

    def seed(self):
        self._populate_individual_investors(self.INVESTOR_COUNT)
        print(f"{InvestorIndividual.objects.count()} individual investors in the db.\n")


    def _populate_individual_investors(self, count):
        """Seeder for fake individuals"""
        print('seeding individuals...')
        for i in range(1,count+1):
            name = self.faker.name()
            company = self.faker.company()
            position = self.faker.job()
            email = self.faker.email()
            primary_phone_number = self.faker.phone_number()
            secondary_phone_number = self.faker.phone_number()
            number_of_portfolio_companies = random.randint(0,9)
            number_of_personal_companies = number_of_portfolio_companies - random.randint(0,number_of_portfolio_companies)
            number_of_partner_companies = number_of_portfolio_companies - number_of_personal_companies
            number_of_exits = random.randint(0,number_of_portfolio_companies)
            part_of_incubator = bool(random.getrandbits(1))

            investor_individual = InvestorIndividual.objects.create(
                name=name,
                AngelListLink="https://www.AngelList.com",
                CrunchbaseLink="https://www.Crunchbase.com",
                LinkedInLink="https://www.LinkedIn.com",
                Company=company,
                Position=position,
                Email=email,
                PrimaryNumber=primary_phone_number,
                SecondaryNumber=secondary_phone_number,
                NumberOfPortfolioCompanies=number_of_portfolio_companies,
                NumberOfPersonalInvestments = number_of_personal_companies,
                NumberOfPartnerInvestments = number_of_partner_companies,
                PartOfIncubator = part_of_incubator,
                NumberOfExits = number_of_exits,
            )
            investor_individual.save()

            address1 = self.faker.building_number()
            address2 = self.faker.street_address()
            city = self.faker.city()
            postcode = self.faker.postcode()
            state = self.faker.country_code()
            country = self.faker.country()
            addr = ResidentialAddress.objects.create(
                address_line1=address1,
                address_line2=address2,
                postal_code=postcode,
                city=city,
                state=state,
                country=country,
                individual=investor_individual
            )
            addr.save()
            print(F"InvestorIndividual with id({investor_individual.id}) has been seeded.")
