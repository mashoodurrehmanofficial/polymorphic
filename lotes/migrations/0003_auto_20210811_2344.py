# Generated by Django 3.1.5 on 2021-08-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lotes', '0002_alter_lote_fecha_salida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
