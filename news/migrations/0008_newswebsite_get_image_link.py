# Generated by Django 4.0.5 on 2022-07-07 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_article_link_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='newswebsite',
            name='get_image_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='news.imagewebsite'),
        ),
    ]
