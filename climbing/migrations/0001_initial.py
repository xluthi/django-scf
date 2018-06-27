# Generated by Django 2.0.6 on 2018-06-11 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=100, verbose_name='Lastname')),
                ('firstname', models.CharField(max_length=100, verbose_name='Firstname')),
                ('gender', models.CharField(choices=[('M', 'male'), ('F', 'female')], default='M', max_length=1, verbose_name='Gender')),
                ('birthdate', models.DateField(verbose_name='Birthdate')),
                ('club', models.CharField(max_length=100, verbose_name='Club')),
                ('nationality', models.CharField(default='BEL', max_length=3, verbose_name='Nationality')),
                ('category', models.CharField(choices=[('D', 'D'), ('C', 'C'), ('B', 'B'), ('A', 'A'), ('J', 'Junior'), ('S', 'Senior'), ('V', 'Veteran'), ('P', 'para')], default='C', max_length=1, verbose_name='Category')),
            ],
        ),
    ]