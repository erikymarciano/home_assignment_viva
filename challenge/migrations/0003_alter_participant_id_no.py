# Generated by Django 4.0 on 2023-03-06 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0002_alter_competition_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='id_no',
            field=models.IntegerField(unique=True),
        ),
    ]