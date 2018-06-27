# Generated by Django 2.0.6 on 2018-06-11 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boulder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True, verbose_name='ID number')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Description')),
                ('top_value', models.PositiveIntegerField(default=1000, verbose_name='Value for top')),
                ('zone_value', models.PositiveIntegerField(default=0, verbose_name='Value for zone')),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Event date')),
                ('description', models.TextField(verbose_name='Event description')),
            ],
        ),
        migrations.AddField(
            model_name='boulder',
            name='competition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='climbing.Competition'),
        ),
    ]
