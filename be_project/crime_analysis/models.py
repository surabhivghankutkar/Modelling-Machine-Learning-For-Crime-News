from django.db import models
from django.utils.translation import gettext as _
import datetime
# Create your models here.
class NewspaperURL(models.Model):
    enter_url = models.CharField(max_length=100)

class Data(models.Model):
    newspaper_name = models.CharField(max_length=100)
    headline = models.CharField(max_length=100)
    summary = models.CharField(max_length=400)
    date_of_news = models.DateField(_("Date"), default=datetime.date.today)

class ExportPDF(models.Model):
    export_pdf = models.CharField(max_length=100)