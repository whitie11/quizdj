# Generated by Django 4.0.5 on 2022-07-16 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myChannels', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='active_channel',
            old_name='channel_layer',
            new_name='channel_nane',
        ),
    ]
