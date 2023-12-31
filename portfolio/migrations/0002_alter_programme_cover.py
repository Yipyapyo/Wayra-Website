# Generated by Django 4.1.2 on 2023-03-19 20:29

import django.core.validators
from django.db import migrations, models
import portfolio.models.programme_model


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='cover',
            field=models.ImageField(blank=True, upload_to=portfolio.models.programme_model.get_path, validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
