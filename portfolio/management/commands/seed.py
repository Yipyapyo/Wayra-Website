import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from portfolio.models import User
from django.db import IntegrityError
import random
from decimal import Decimal


class Command(BaseCommand):

    def __init__(self):
        super().__init__()

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

        print(f"done.")
        print(f"{User.objects.count()} users in the db.")