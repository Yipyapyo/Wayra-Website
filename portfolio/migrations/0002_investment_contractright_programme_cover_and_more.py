# Generated by Django 4.1.2 on 2023-03-03 12:42

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='contractRight',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programme',
            name='cover',
            field=models.ImageField(blank=True, upload_to='', validators=[django.core.validators.validate_image_file_extension]),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='', validators=[django.core.validators.validate_image_file_extension]),
        ),
        migrations.AlterField(
            model_name='investment',
            name='dateInvested',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 3, 3))]),
        ),
        migrations.AlterField(
            model_name='pastexperience',
            name='end_year',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
