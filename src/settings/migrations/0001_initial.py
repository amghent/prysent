# Generated by Django 4.1 on 2022-10-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Settings',
            },
        ),
        migrations.AddConstraint(
            model_name='setting',
            constraint=models.UniqueConstraint(fields=('key',), name='ux_settings_key'),
        ),
    ]