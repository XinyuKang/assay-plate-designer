# Generated by Django 4.2.5 on 2023-09-22 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('384', '384'), ('96', '96')], default='384', max_length=3)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reagent', models.CharField(max_length=20)),
                ('antibody', models.CharField(default='empty', max_length=40)),
                ('concentration', models.FloatField(default='0.0')),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('plate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Experiment.plate')),
            ],
        ),
    ]
