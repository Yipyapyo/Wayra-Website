import os
import random
import shutil
from io import BytesIO

from django.conf.global_settings import STATIC_ROOT
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import SimpleUploadedFile

from portfolio.seeders import Seeder
from portfolio.models import Programme, Company, Portfolio_Company, Individual
from vcpms.settings import MEDIA_ROOT, STATIC_URL, BASE_DIR


class ProgrammeSeeder(Seeder):
    PROGRAMME_COUNT = 5

    def seed(self):
        self._create_programme(self.PROGRAMME_COUNT)
        print(f"{Programme.objects.count()} programmes in the db.\n")

    def _get_objects_from_models(self, model, index, slice_size):
        random_number_of_object = random.randint(1, slice_size)
        objects = list(
            model.objects.filter(id__in=range(index * slice_size, index * slice_size + random_number_of_object)))
        return objects

    def _create_programme(self, count):
        # TODO: Reset media directory should write a proper way soon
        shutil.rmtree(MEDIA_ROOT)
        os.mkdir(MEDIA_ROOT)
        for i in range(1,count+1):
            try:
                Programme.objects.get(name=f"Accelerator Programme {i}", cohort=1)
                print(f"Accelerator Programme {i} has already been seeded.")
            except ObjectDoesNotExist:
                image_file = BytesIO()
                image_file.write(open(os.path.join(BASE_DIR,'portfolio\\seeders\\resource\\edison_programme.png'), 'rb').read())
                image_file.seek(0)
                file_data = SimpleUploadedFile("edison_programme.png", image_file.read(), content_type="image/png")

                accelerator_1 = Programme.objects.create(
                    name=f"Accelerator Programme {i}",
                    cohort=1,
                    cover=file_data
                )
                for company in self._get_objects_from_models(Company, i, Company.objects.count() // count):
                    accelerator_1.partners.add(company)
                for p_company in self._get_objects_from_models(Portfolio_Company, i, Portfolio_Company.objects.count() // count):
                    accelerator_1.participants.add(p_company)
                for individual in self._get_objects_from_models(Individual, i, Individual.objects.count() // count):
                    accelerator_1.coaches_mentors.add(individual)
                accelerator_1.save()
                print(f"Accelerator Programme {i} has been seeded.")