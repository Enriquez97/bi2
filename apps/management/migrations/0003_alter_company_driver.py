# Generated by Django 5.0 on 2024-06-11 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_company_database_company_driver_company_server_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='driver',
            field=models.CharField(default='ODBC Driver 17 for SQL Server', max_length=255, null=True),
        ),
    ]
