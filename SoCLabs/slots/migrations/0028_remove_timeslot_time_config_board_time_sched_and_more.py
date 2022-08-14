# Generated by Django 4.0.4 on 2022-07-03 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_course_code'),
        ('slots', '0027_ipaddress_cam_port'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='time_config',
        ),
        migrations.AddField(
            model_name='board',
            name='time_sched',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='slots.timeschedule'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.CreateModel(
            name='StartDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
    ]