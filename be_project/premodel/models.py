from django.db import models
from django.utils.translation import gettext as _
import datetime
# Create your models here.
class ExportPDF(models.Model):
    export_pdf = models.CharField(max_length=100)