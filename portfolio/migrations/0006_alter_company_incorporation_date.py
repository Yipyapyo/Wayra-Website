# Generated by Django 4.1.2 on 2023-02-15 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_company_company_registration_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='incorporation_date',
            field=models.DateField(auto_now=True),
        ),
    ]