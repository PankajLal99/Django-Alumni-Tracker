# Generated by Django 3.0.2 on 2020-04-12 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0035_auto_20200412_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='post_img',
        ),
        migrations.AddField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='static/images/bg.jpg', upload_to='AlumniTracker/images'),
        ),
    ]
