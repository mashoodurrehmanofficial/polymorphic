# Generated by Django 3.1.1 on 2021-08-23 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crias', '0007_cria_alimentar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cria',
            name='alimentar',
        ),
    ]
