# Generated by Django 3.1.5 on 2021-08-13 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimento', '0003_auto_20210811_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimento',
            name='cantidad',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='alimento',
            name='costo',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
