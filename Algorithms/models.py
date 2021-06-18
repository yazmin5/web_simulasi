from django.db import models
from datetime import date
from django.utils import timezone
from datetime import datetime

# ------------------------------- Epirank -----------------------------
class Documents(models.Model): 
    name = models.CharField(max_length=500, null=True)
    date_input = models.DateTimeField(default=datetime.now(), null=True)
    uploaded_file_berangkat = models.FileField(null=True)
    uploaded_file_pulang = models.FileField(null=True)

    def __str__(self):
        return self.name

# ------------------------------- PageRank -----------------------------

# Choices for PageRank form
wilayah =[('east_java','Jawa Timur'),
         ('central_java','Jawa Tengah'),
         ('bali', 'Bali')]

# Get current date
date = datetime.now()

file_path = "uploads/{}/{}/{}/".format(date.year, date.month, date.day)

class DocumentsPageRank(models.Model): 
    Nama = models.CharField(max_length=100, null=True, verbose_name='Nama ')
    Tanggal = models.DateTimeField(default=datetime.now(), null=True, verbose_name='Tanggal ')
    Wilayah = models.CharField(max_length=12, choices=wilayah, default='east_java', verbose_name='Wilayah ')
    File_GDP = models.FileField(null=True, verbose_name='File PDB Regional ', upload_to=file_path)
    File_MAN = models.FileField(null=True, verbose_name='File Jumlah Penduduk Laki-Laki ', upload_to=file_path)
    File_UNEM = models.FileField(null=True, verbose_name='File Tingkat Pengangguran ', upload_to=file_path)
    File_CRIM = models.FileField(null=True, verbose_name='File Jumlah Kejahatan ', upload_to=file_path)
    File_DENS = models.FileField(null=True, verbose_name='File Kepadatan Penduduk ', upload_to=file_path)
    File_LIT = models.FileField(null=True, verbose_name='File Angka Melek Huruf ', upload_to=file_path)
    File_INF = models.FileField(null=True, verbose_name='File Rata-Rata Pendapatan Pekerja Informal ', upload_to=file_path)
    File_MIN = models.FileField(null=True, verbose_name='File Upah Minimum Regional ', upload_to=file_path)
    File_Cases = models.FileField(null=True, verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 ', upload_to=file_path)

    def __str__(self):
        return self.name

# ------------------------------- Distance Decay PageRank -----------------------------

# Write models' class for Distance Decay PageRank here.