# Generated by Django 5.0 on 2024-04-15 20:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler_data', '0003_alter_storeprocedure_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataconfig',
            name='config_sp_name',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='storeprocedure',
            name='config',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='handler_data.dataconfig'),
        ),
    ]
