# Generated by Django 3.2.5 on 2021-07-27 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crias', '0002_cria_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='cria',
            name='vaca_madura_id',
            field=models.IntegerField(null=True),
        ),
    ]
