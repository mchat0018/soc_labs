# Generated by Django 4.0.1 on 2022-04-08 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0017_remove_board_time_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='board_no',
            field=models.IntegerField(default=1),
        ),
    ]
