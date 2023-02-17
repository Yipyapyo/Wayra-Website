from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from faker import Faker
from portfolio.models import User, Company
import random


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("seeding...")
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

        # Create Petra Pickles (Administrator)
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

        # Create 100 auto generated students with requests, lessons and transactions
        self.populate_companies()

        print(f"done.")
        print(f"{User.objects.count()} users in the db.")

    def populate_companies(self):
        self.stdout.write('seeding admin...')
        for i in range(10):
            company_name1 = self.faker.company()
            company_name2 = self.faker.company()
            crn = random.randint(0,10**8)
            address = self.faker.address()
            city = self.faker.city()
            Company.objects.create(name=company_name1,
                                         company_registration_number=crn,
                                         trading_names=company_name1,
                                         previous_names=company_name2,
                                         registered_address=address,
                                         jurisdiction=city,)
