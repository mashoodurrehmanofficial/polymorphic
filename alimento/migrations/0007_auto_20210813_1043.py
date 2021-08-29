# Generated by Django 3.1.5 on 2021-08-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alimento', '0006_auto_20210813_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlimentoExport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=45, null=True)),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fecha_export', models.DateField()),
                ('destino', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='alimento',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]