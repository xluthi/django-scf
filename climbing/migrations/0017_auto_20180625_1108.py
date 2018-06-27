# Generated by Django 2.0.6 on 2018-06-25 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0016_remove_result_competition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='athlete',
            options={'ordering': ['lastname', 'firstname']},
        ),
        migrations.AlterModelOptions(
            name='boulder',
            options={'ordering': ['number']},
        ),
        migrations.AddField(
            model_name='competition',
            name='location',
            field=models.CharField(blank=True, max_length=100, verbose_name='Location'),
        ),
    ]
