# Generated by Django 4.0.5 on 2022-07-07 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_searchables_website_alter_newswebsite_get_news_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchables',
            old_name='name',
            new_name='title',
        ),
    ]
