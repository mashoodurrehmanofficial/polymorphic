# Generated by Django 3.1.5 on 2021-08-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preñez', '0002_preñez_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metodopreñez',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='preñez',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
