# Generated by Django 4.0.5 on 2022-09-27 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizAdmin', '0002_question_correctans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='startTime',
        ),
        migrations.RemoveField(
            model_name='question',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='question',
            name='type',
        ),
    ]
