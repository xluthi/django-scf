# Generated by Django 2.0.6 on 2018-06-14 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0015_remove_athlete_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='competition',
        ),
    ]
