# Generated by Django 3.1.5 on 2021-08-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacas', '0003_remove_vaca_tiempo_preñez'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaca',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]