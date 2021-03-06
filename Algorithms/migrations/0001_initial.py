# Generated by Django 3.1.6 on 2021-06-21 01:33

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, null=True)),
                ('date_input', models.DateTimeField(default=datetime.datetime(2021, 6, 21, 8, 33, 51, 814268), null=True)),
                ('uploaded_file_berangkat', models.FileField(null=True, upload_to='')),
                ('uploaded_file_pulang', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentsDDPR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nama', models.CharField(max_length=100, null=True, verbose_name='Nama ')),
                ('Tanggal', models.DateTimeField(default=datetime.datetime(2021, 6, 21, 8, 33, 51, 815249), null=True, verbose_name='Tanggal ')),
                ('File_Jarak', models.FileField(null=True, upload_to='uploads/2021/6/21/', verbose_name='File OD Matrix Beserta Jarak Antar Stasiun ')),
                ('File_Kasus_Stasiun', models.FileField(null=True, upload_to='uploads/2021/6/21/', verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 Per Stasiun ')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentsPageRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Wilayah', models.CharField(choices=[('Jawa Timur', 'Jawa Timur'), ('Jawa Tengah', 'Jawa Tengah'), ('Bali', 'Bali')], default='east_java', max_length=12, verbose_name='Wilayah ')),
                ('Tanggal', models.DateTimeField(default=datetime.datetime(2021, 6, 21, 8, 33, 51, 814807), null=True, verbose_name='Tanggal ')),
                ('File_Matriks_OD', models.FileField(null=True, upload_to='uploads/2021/6/21/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'], message='File harus dalam format .xlsx')], verbose_name='File Matriks OD ')),
                ('File_Cases', models.FileField(null=True, upload_to='uploads/2021/6/21/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'], message='File harus dalam format .csv')], verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 ')),
            ],
        ),
    ]
