# Generated by Django 3.2.5 on 2021-08-23 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimento', '0008_alimentoexport_alimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimento',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='alimentoexport',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]