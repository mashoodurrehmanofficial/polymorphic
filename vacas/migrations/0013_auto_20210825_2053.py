# Generated by Django 3.1.1 on 2021-08-25 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacas', '0012_alter_raza_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raza',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vaca',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='BornHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('vaca', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vacas.vaca')),
            ],
        ),
    ]
