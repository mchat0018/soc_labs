# Generated by Django 4.0.4 on 2022-06-10 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_description'),
        ('slots', '0023_timeconfig_slot_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='board_no',
        ),
        migrations.RemoveField(
            model_name='board',
            name='time_sched',
        ),
        migrations.RemoveField(
            model_name='ipaddress',
            name='board_no',
        ),
        migrations.RemoveField(
            model_name='timeconfig',
            name='no_of_boards',
        ),
        migrations.AddField(
            model_name='board',
            name='board_name',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='board_name',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='board_type',
            field=models.CharField(choices=[('Basys3', 'Basys3'), ('Zynq', 'Zynq'), ('Zedboard', 'Zedboard')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='timeconfig',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='timeschedule',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AlterField(
            model_name='board',
            name='ip_addr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='slots.ipaddress'),
        ),
    ]