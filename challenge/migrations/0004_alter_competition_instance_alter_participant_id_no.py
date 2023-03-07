# Generated by Django 4.0 on 2023-03-07 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0003_alter_participant_id_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenge.instance'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='id_no',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
