# Generated by Django 3.1.6 on 2021-06-13 04:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Algorithms', '0003_auto_20210610_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Angka_Melek_Huruf',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Jumlah_Kejahatan',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Jumlah_Penduduk_Laki_Laki',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Kepadatan_Penduduk',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_PDB_Regional',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Rata_Rata_Pendapatan_Pekerja_Informal',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Tingkat_Pengangguran',
        ),
        migrations.RemoveField(
            model_name='documentspagerank',
            name='File_Upah_Minimum_Regional',
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_CRIM',
            field=models.FileField(null=True, upload_to='', verbose_name='File Jumlah Kejahatan '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_Cases',
            field=models.FileField(null=True, upload_to='', verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_DENS',
            field=models.FileField(null=True, upload_to='', verbose_name='File Kepadatan Penduduk '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_GDP',
            field=models.FileField(null=True, upload_to='static/documents/filename/%Y/%m/%d/', verbose_name='File PDB Regional '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_INF',
            field=models.FileField(null=True, upload_to='', verbose_name='File Rata-Rata Pendapatan Pekerja Informal '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_LIT',
            field=models.FileField(null=True, upload_to='', verbose_name='File Angka Melek Huruf '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_MAN',
            field=models.FileField(null=True, upload_to='', verbose_name='File Jumlah Penduduk Laki-Laki '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_MIN',
            field=models.FileField(null=True, upload_to='', verbose_name='Upah Minimum Regional '),
        ),
        migrations.AddField(
            model_name='documentspagerank',
            name='File_UNEM',
            field=models.FileField(null=True, upload_to='', verbose_name='File Tingkat Pengangguran '),
        ),
        migrations.AlterField(
            model_name='documents',
            name='date_input',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 13, 11, 9, 1, 787544), null=True),
        ),
        migrations.AlterField(
            model_name='documentspagerank',
            name='Tanggal',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 13, 11, 9, 1, 788077), null=True),
        ),
        migrations.AlterField(
            model_name='documentspagerank',
            name='Wilayah',
            field=models.CharField(choices=[('east_java', 'Jawa Timur'), ('central_java', 'Jawa Tengah'), ('bali', 'Bali')], default='east_java', max_length=12),
        ),
    ]
