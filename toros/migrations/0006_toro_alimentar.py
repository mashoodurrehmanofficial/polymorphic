# Generated by Django 3.1.1 on 2021-08-19 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toros', '0005_toro_fecha_processm'),
    ]

    operations = [
        migrations.AddField(
            model_name='toro',
            name='alimentar',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]