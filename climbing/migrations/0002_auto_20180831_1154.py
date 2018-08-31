# Generated by Django 2.0.6 on 2018-08-31 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='boulder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='climbing.Boulder'),
        ),
        migrations.AlterField(
            model_name='result',
            name='competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='climbing.Competitor'),
        ),
    ]
