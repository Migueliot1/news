# Generated by Django 4.0.5 on 2022-08-11 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_activity_user_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='vote_total',
        ),
        migrations.RemoveField(
            model_name='message',
            name='name',
        ),
    ]
