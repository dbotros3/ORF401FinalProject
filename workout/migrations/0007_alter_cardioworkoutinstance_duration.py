# Generated by Django 4.1.13 on 2024-04-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0006_alter_cardioworkoutinstance_average_heart_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardioworkoutinstance',
            name='duration',
            field=models.IntegerField(blank=True, help_text='Duration of the workout in minutes', null=True),
        ),
    ]
