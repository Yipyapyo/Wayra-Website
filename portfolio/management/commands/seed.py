from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_countries.fields import Country
from phonenumber_field.phonenumber import PhoneNumber

from portfolio.models import User, Individual, Company, Portfolio_Company, Programme, ResidentialAddress
from faker import Faker
from portfolio.models import User, Company, ResidentialAddress, Individual
import random


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("seeding...")
        self.create_standard_user()

        # Create Petra Pickles (Administrator)
        self.create_admin_user()

        # Create 100 auto generated students with requests, lessons and transactions

        print(f"done.")
        print(f"{User.objects.count()} users in the db.")

        self.create_individual()

        self.create_company()

        self.create_porfolio_company()

        self.create_programme()

        self.populate_companies()

        self.populate_individuals()

        print(f"done.")
        print(f"{User.objects.count()} users in the db.")

    def create_programme(self):
        try:
            Programme.objects.get(name="Accelerator Programme", cohort=1)
            print("Accelerator Programme 1 has already seeded.")

        except ObjectDoesNotExist:
            accelerator_1 = Programme.objects.create(
                name="Accelerator Programme",
                cohort=1,
            )
            accelerator_1.partners.add(Company.objects.get(name="Default Ltd"))
            accelerator_1.participants.add(Portfolio_Company.objects.get(name="Child Ltd"))
            accelerator_1.coaches_mentors.add(Individual.objects.get(name="Jemma Doe"))
            accelerator_1.save()
            print("Accelerator Programme 1 has been seeded.")

    def create_porfolio_company(self):
        try:
            Portfolio_Company.objects.get(name="Child Ltd")
            print("Child Ltd has already seeded.")

        except ObjectDoesNotExist:
            company_name1 = self.faker.company()
            company_name2 = self.faker.company()
            crn = random.randint(0, 10 ** 8)
            address = self.faker.address()
            city = self.faker.city()

            child_ltd = Portfolio_Company.objects.create(
                name="Child Ltd",
                company_registration_number=crn,
                trading_names=company_name1,
                previous_names=company_name2,
                registered_address=address,
                jurisdiction=city,
                incorporation_date=timezone.now(),
                wayra_number="WN-1"
            )
            child_ltd.save()
            print("Child Ltd has been seeded.")

    def create_company(self):
        try:
            Company.objects.get(name="Default Ltd")
            print("Default Ltd has already seeded.")

        except ObjectDoesNotExist:
            company_name1 = self.faker.company()
            company_name2 = self.faker.company()
            crn = random.randint(0, 10 ** 8)
            address = self.faker.address()
            city = self.faker.city()
            default_ltd = Company.objects.create(name="Default Ltd",
                                                 company_registration_number=crn,
                                                 trading_names=company_name1,
                                                 previous_names=company_name2,
                                                 registered_address=address,
                                                 jurisdiction=city, )
            default_ltd.save()
            print("Default Ltd has been seeded.")

    def create_standard_user(self):
        try:
            User.objects.get(email="john.doe@example.org")
            print("john doe has already seeded.")

        except (ObjectDoesNotExist):
            user_john = User.objects.create_user(
                email="john.doe@example.org",
                password="Password123",
                first_name="John",
                last_name="Doe",
                phone="+447312345678"
            )
            user_john.save()
            print("john doe has been seeded.")

    def create_admin_user(self):
        try:
            User.objects.get(email="petra.pickles@example.org")
            print("petra pickles has already seeded.")

        except (ObjectDoesNotExist):
            user_petra = User.objects.create_superuser(
                email="petra.pickles@example.org",
                password="Password123",
                first_name="Petra",
                last_name="Pickles",
                phone="+447312345678"
            )
            user_petra.save()
            print("petra has been seeded.")

    def create_individual(self):
        """Seeder for individual"""
        try:
            Individual.objects.get(name="Jemma Doe")
            print("Jemma Doe has already seeded.")
        except ObjectDoesNotExist:
            jemma_individual = Individual.objects.create(
                name="Jemma Doe",
                AngelListLink="https://www.AngelList.com",
                CrunchbaseLink="https://www.Crunchbase.com",
                LinkedInLink="https://www.LinkedIn.com",
                Company="exampleCompany",
                Position="examplePosition",
                Email="test@gmail.com",
                PrimaryNumber=PhoneNumber.from_string("+447975777666"),
                SecondaryNumber=PhoneNumber.from_string("+441325777655")
            )
            jemma_individual.save()

            print("Jemma Doe has been seeded.")

        jemma_individual = Individual.objects.get(name="Jemma Doe")
        try:
            ResidentialAddress.objects.get(individual=jemma_individual)
            print("Jemma's address has already seeded.")
        

        except ObjectDoesNotExist:
            addr = ResidentialAddress.objects.create(
                address_line1="testAdress1",
                address_line2="testAdress2",
                postal_code="testCode",
                city="testCity",
                state="testState",
                country=Country("AD"),
                individual=jemma_individual
            )
            addr.save()
            print("Jemma's address has been seeded.")

    def populate_companies(self):
        self.stdout.write('seeding admin...')
        for i in range(10):
            company_name1 = self.faker.company()
            company_name2 = self.faker.company()
            crn = random.randint(0, 10 ** 8)
            address = self.faker.address()
            city = self.faker.city()
            Company.objects.create(name=company_name1,
                                   company_registration_number=crn,
                                   trading_names=company_name1,
                                   previous_names=company_name2,
                                   registered_address=address,
                                   jurisdiction=city, )

    def populate_individuals(self):
        """Seeder for fake individuals"""
        self.stdout.write('seeding admin...')
        for i in range(15):
            name = self.faker.name()
            company = self.faker.company()
            position = self.faker.job()
            email = self.faker.email()
            primary_phone_number = self.faker.phone_number()
            secondary_phone_number = self.faker.phone_number()

            individual = Individual.objects.create(
                name=name,
                AngelListLink="https://www.AngelList.com",
                CrunchbaseLink="https://www.Crunchbase.com",
                LinkedInLink="https://www.LinkedIn.com",
                Company=company,
                Position=position,
                Email=email,
                PrimaryNumber=primary_phone_number,
                SecondaryNumber=secondary_phone_number
            )
            individual.save()

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
                individual=individual
            )
            addr.save()
