# Generated by Django 4.0.4 on 2022-06-22 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0025_ipaddress_board_serial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='time_config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='slots.timeconfig'),
        ),
    ]
