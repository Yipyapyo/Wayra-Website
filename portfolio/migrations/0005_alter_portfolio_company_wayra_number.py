# Generated by Django 4.1.2 on 2023-03-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_alter_portfolio_company_parent_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio_company',
            name='wayra_number',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
