# Generated by Django 3.0.2 on 2020-04-01 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0013_auto_20200401_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrapper_data',
            old_name='degress_year',
            new_name='degree_year',
        ),
    ]