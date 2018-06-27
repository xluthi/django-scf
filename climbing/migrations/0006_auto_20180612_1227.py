# Generated by Django 2.0.6 on 2018-06-12 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0005_subcompetition_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='subcompetition',
        ),
        migrations.AddField(
            model_name='result',
            name='competition',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='climbing.Competition'),
            preserve_default=False,
        ),
    ]