# Generated by Django 3.1.1 on 2021-08-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0005_auto_20210823_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='produccion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
