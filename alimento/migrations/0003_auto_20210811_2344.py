# Generated by Django 3.1.5 on 2021-08-11 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacas', '0004_auto_20210811_2344'),
        ('alimento', '0002_alimento_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimento',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='alimento',
            name='vaca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacas.vaca'),
        ),
    ]
