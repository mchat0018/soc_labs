# Generated by Django 4.0.1 on 2022-01-28 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayschedule',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
