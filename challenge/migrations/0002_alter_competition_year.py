# Generated by Django 4.0 on 2023-03-05 21:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1900)]),
        ),
    ]