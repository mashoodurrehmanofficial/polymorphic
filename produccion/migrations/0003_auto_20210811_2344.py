# Generated by Django 3.1.5 on 2021-08-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produccion', '0002_produccion_usuario'),
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
