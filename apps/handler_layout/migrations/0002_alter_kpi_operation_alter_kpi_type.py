# Generated by Django 5.0 on 2024-04-16 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handler_layout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='operation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='kpi',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
