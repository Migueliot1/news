# Generated by Django 4.0.5 on 2022-07-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_answer_answer_to_answer_answers_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_answer',
            field=models.BooleanField(default=False),
        ),
    ]
