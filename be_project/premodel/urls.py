from django.conf.urls import url
from . import views

app_name = 'premodel'

urlpatterns = [
    url(r'^prehome/$', views.premodel_home, name = "prehome"),
    url(r'^export/$', views.export_to_pdf, name="export"),
]