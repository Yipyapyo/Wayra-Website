# Generated by Django 4.1.2 on 2023-02-09 15:29

from django.db import migrations
import portfolio.manager


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', portfolio.manager.UserManager()),
            ],
        ),
    ]
