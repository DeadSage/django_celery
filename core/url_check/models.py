from django.db import models


# Create your models here.

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    result = models.BooleanField(blank=True, null=True)
    calc_time = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
