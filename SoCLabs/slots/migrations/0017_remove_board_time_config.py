# Generated by Django 4.0.1 on 2022-02-27 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0016_board_time_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='time_config',
        ),
    ]
