# Generated by Django 3.0.2 on 2020-04-08 05:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0021_auto_20200408_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+919999999'. Up to 10 digits allowed.", regex='^[789]\\d{9}$ ')]),
        ),
    ]
