# Generated by Django 3.1.6 on 2021-04-30 07:19

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari_jam', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('date_input', models.DateTimeField(default=datetime.date.today, null=True)),
                ('uploaded_file_berangkat', models.FileField(null=True, upload_to='')),
                ('uploaded_file_pulang', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]
