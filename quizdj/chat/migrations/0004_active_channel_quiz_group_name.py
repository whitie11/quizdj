# Generated by Django 4.0.5 on 2022-07-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_rename_channel_nane_active_channel_channel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='active_channel',
            name='quiz_group_name',
            field=models.CharField(default='lobby', max_length=200),
            preserve_default=False,
        ),
    ]
