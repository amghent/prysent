# Generated by Django 4.0.6 on 2022-10-05 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_ascii', models.CharField(max_length=100)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('country', models.CharField(max_length=100)),
                ('iso2', models.CharField(max_length=2)),
                ('iso3', models.CharField(max_length=3)),
                ('admin_name', models.CharField(max_length=100)),
                ('capital', models.CharField(max_length=100)),
                ('population', models.BigIntegerField()),
            ],
        ),
    ]
