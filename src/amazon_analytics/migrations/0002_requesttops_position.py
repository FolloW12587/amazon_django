# Generated by Django 2.2.5 on 2021-03-12 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesttops',
            name='position',
            field=models.IntegerField(default=0, verbose_name='Позиция запроса'),
            preserve_default=False,
        ),
    ]
