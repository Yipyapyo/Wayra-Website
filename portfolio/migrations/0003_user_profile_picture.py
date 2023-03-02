# Generated by Django 4.1.2 on 2023-03-02 18:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_pastexperience_end_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='', validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]