# Generated by Django 4.0.6 on 2022-10-05 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('html_file', models.CharField(default=None, max_length=1024, null=True)),
                ('cached_html', models.CharField(default=None, max_length=1024, null=True)),
                ('cached_until', models.DateTimeField(default=None, null=True)),
                ('generated', models.BooleanField(default=False)),
                ('generation_timeout', models.DateTimeField(default=None, null=True)),
                ('generation_status', models.IntegerField(default=0)),
                ('generation_message', models.TextField(default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Cached',
            },
        ),
        migrations.AddConstraint(
            model_name='cache',
            constraint=models.UniqueConstraint(fields=('html_file',), name='ux_cache_html_file'),
        ),
    ]
