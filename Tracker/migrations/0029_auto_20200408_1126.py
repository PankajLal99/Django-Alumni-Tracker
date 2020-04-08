# Generated by Django 3.0.2 on 2020-04-08 05:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0028_auto_20200408_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?\\d[\\d -]{8,12}\\d')]),
        ),
    ]
