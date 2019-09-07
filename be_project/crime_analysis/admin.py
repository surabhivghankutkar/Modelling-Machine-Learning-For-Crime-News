from django.contrib import admin
from .models import NewspaperURL, Data

# Register your models here.
admin.site.register(NewspaperURL)
admin.site.register(Data)