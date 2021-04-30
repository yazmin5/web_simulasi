from django.db import models
from datetime import date
from django.utils import timezone

# Create your models here.
class Documents(models.Model): 
    name = models.CharField(max_length=500, null=True)
    date_input = models.DateTimeField(default=date.today, null=True)
    uploaded_file_berangkat = models.FileField(null=True)
    uploaded_file_pulang = models.FileField(null=True)

    def __str__(self):
        return self.name