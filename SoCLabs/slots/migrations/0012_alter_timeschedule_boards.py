# Generated by Django 4.0.1 on 2022-02-15 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0011_remove_timeschedule_board1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeschedule',
            name='boards',
            field=models.ManyToManyField(to='slots.Boards'),
        ),
    ]
