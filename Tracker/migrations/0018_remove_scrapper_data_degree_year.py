# Generated by Django 3.0.2 on 2020-04-01 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0017_auto_20200401_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrapper_data',
            name='degree_year',
        ),
    ]