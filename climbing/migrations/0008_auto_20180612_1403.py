# Generated by Django 2.0.6 on 2018-06-12 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climbing', '0007_auto_20180612_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(max_length=3, verbose_name='Code'),
        ),
    ]