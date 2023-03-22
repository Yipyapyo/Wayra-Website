# Generated by Django 4.1.2 on 2023-03-20 18:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='portfolio.individual'),
        ),
        migrations.AddField(
            model_name='document',
            name='programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='portfolio.programme'),
        ),
        migrations.AlterField(
            model_name='document',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='portfolio.company'),
        ),
        migrations.AlterField(
            model_name='document',
            name='file_name',
            field=models.CharField(max_length=254, validators=[django.core.validators.RegexValidator(
                message='Document name must consist of up to 254 valid characters: 0-9 a-z A-Z _ \\ - . and spaces',
                regex='^[0-9a-zA-Z_\\-. ]+$')]),
        ),
        migrations.AddConstraint(
            model_name='document',
            constraint=models.CheckConstraint(check=models.Q(
                models.Q(('company__isnull', False), ('individual__isnull', True), ('programme__isnull', True)),
                models.Q(('company__isnull', True), ('individual__isnull', False), ('programme__isnull', True)),
                models.Q(('company__isnull', True), ('individual__isnull', True), ('programme__isnull', False)),
                _connector='OR'), name='portfolio_document_company_or_individual_or_programme'),
        ),
    ]
