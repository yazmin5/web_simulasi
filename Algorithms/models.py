from django.db import models
from datetime import date
from django.utils import timezone
from datetime import datetime
from django.core.validators import FileExtensionValidator

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
wilayah =[('Jawa Timur','Jawa Timur'),
         ('Jawa Tengah','Jawa Tengah'),
         ('Bali', 'Bali')]

# Get current date
date = datetime.now()

file_path = "uploads/{}/{}/{}/".format(date.year, date.month, date.day)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class DocumentsPageRank(models.Model): 
    Wilayah = models.CharField(max_length=12, choices=wilayah, default='east_java', verbose_name='Wilayah ')
    Tanggal = models.DateTimeField(default=datetime.now(), null=True, verbose_name='Tanggal ')
    File_Matriks_OD = models.FileField(null=True, verbose_name='File Matriks OD ', validators=[FileExtensionValidator(allowed_extensions=['xlsx'], message='File Matriks OD harus dalam format .xlsx')], upload_to=file_path)
    File_Cases = models.FileField(null=True, verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 ', validators=[FileExtensionValidator(allowed_extensions=['csv'], message='File Jumlah Kasus Terkonfirmasi Covid-19 harus dalam format .csv')], upload_to=file_path)

    def __str__(self):
        return self.name

# ------------------------------- Distance Decay PageRank -----------------------------

# Get current date
date = datetime.now()

file_path = "uploads/{}/{}/{}/".format(date.year, date.month, date.day)

class DocumentsDDPR(models.Model): 
    Nama = models.CharField(max_length=100, null=True, verbose_name='Nama ')
    Tanggal = models.DateTimeField(default=datetime.now(), null=True, verbose_name='Tanggal ')
    File_Jarak = models.FileField(null=True, verbose_name='File OD Matrix Beserta Jarak Antar Stasiun ', upload_to=file_path)
    File_Kasus_Stasiun = models.FileField(null=True, verbose_name='File Jumlah Kasus Terkonfirmasi Covid-19 Per Stasiun ', upload_to=file_path)
    
    def __str__(self):
        return self.name