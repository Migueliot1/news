# Generated by Django 4.0.5 on 2022-07-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_rename_name_searchables_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='link_main',
            field=models.CharField(max_length=2000, unique=True),
        ),
    ]
