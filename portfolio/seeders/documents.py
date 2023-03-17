import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Document, Company
from portfolio.seeders import Seeder


class DocumentSeeder(Seeder):
    """A seeder for documents."""

    # The number of documents to seed per company (not evenly distributed between companies).
    DOCUMENT_COUNT = 6
    # The number of companies in the db.
    COMPANY_COUNT = 0

    def seed(self):
        # Get the number of companies in the db.
        self.COMPANY_COUNT = Company.objects.count()

        if self.COMPANY_COUNT:
            self._create_documents(self.DOCUMENT_COUNT * self.COMPANY_COUNT)
            print(f"{Document.objects.count()} documents in the db.\n")
        else:
            print(f"Couldn't seed documents. Seed companies first.")

    def _create_documents(self, count):
        for i in range(1, count + 1):
            try:
                Document.objects.get(file_id=i)
                print(f"Document with the id {i} is already seeded.")

            except ObjectDoesNotExist:
                is_file = random.choice([True, False])
                name = self.faker.file_name(category=None)

                # Ensure the file name is unique.
                while Document.objects.filter(file_name=name).exists():
                    name = self.faker.file_name(category=None)

                extension = name.split(".")[-1]
                company_id = random.randint(1, self.COMPANY_COUNT)

                if is_file:
                    document = Document.objects.create(
                        file_name=f"{name}",
                        file_type=extension,
                        company=Company.objects.get(id=company_id),
                        file=SimpleUploadedFile(f"{name}", b"file contents")
                    )
                else:
                    document = Document.objects.create(
                        file_name=f"{name}",
                        file_type="URL",
                        company=Company.objects.get(id=company_id),
                        url="https://www.wayra.uk"
                    )
                document.save()
                print(f"The document with the id {i} has been seeded.")
