from django.conf.urls import url
from . import views

app_name = 'crime_analysis'

urlpatterns = [
    url(r'^$', views.crime_home, name = "home"),
    url(r'^result/$', views.result, name = "result"),
    url(r'^ht/$', views.scrapeht, name="ht"),
    url(r'^ie/$', views.scrapeie, name="ie"),
    url(r'^it/$', views.scrapeit, name="it"),
]