# Generated by Django 4.0.5 on 2022-10-23 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizAdmin', '0003_remove_question_starttime_remove_question_subject_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionGroupList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=20)),
                ('count', models.IntegerField()),
            ],
        ),
    ]