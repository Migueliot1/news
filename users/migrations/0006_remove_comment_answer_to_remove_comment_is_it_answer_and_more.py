# Generated by Django 4.0.5 on 2022-07-26 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_activity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='answer_to',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_it_answer',
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.comment')),
                ('answer_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.answer')),
            ],
            bases=('users.comment',),
        ),
        migrations.AddField(
            model_name='comment',
            name='answers',
            field=models.ManyToManyField(blank=True, to='users.answer'),
        ),
    ]
