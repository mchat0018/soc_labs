# Generated by Django 4.0.4 on 2022-06-16 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='date_due',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lab',
            name='tutorials',
            field=models.FileField(blank=True, upload_to='tutorials/'),
        ),
    ]
