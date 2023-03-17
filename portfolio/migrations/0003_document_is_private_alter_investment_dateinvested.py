# Generated by Django 4.1.2 on 2023-03-17 10:38

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_remove_investment_contractright_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='investment',
            name='dateInvested',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 3, 17))]),
        ),
    ]
