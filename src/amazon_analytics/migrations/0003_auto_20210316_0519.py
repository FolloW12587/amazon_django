# Generated by Django 2.2.5 on 2021-03-16 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_analytics', '0002_requesttops_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='period_date',
            field=models.DateField(unique=True, verbose_name='Дата отчетного периода'),
        ),
    ]
