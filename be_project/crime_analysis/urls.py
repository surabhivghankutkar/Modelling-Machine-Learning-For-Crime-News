from django.conf.urls import url
from . import views

app_name = 'crime_analysis'

urlpatterns = [
    url(r'^$', views.crime_home, name = "crime_home"),
    url(r'^about/$', views.about, name="about"),
    url(r'^result/$', views.result, name = "result"),
    url(r'^analyze_crime/$', views.analyze_crime, name="analyze_crime"),
    url(r'^scrapeht/$', views.scrapeht, name="scrapeht"),
    url(r'^ht/$', views.paper1, name="paper1"),
    url(r'^scrapeasian/$', views.scrapeasian, name="scrapeasian"),
    url(r'^asian/$', views.paper2, name="paper2"),
    url(r'^scracpedaily/$', views.scrapedaily, name="scrapedaily"),
    url(r'^daily/$', views.paper3, name="paper3"),
    url(r'^scrapedecc/$', views.scrapedecc, name="scrapedecc"),
    url(r'^decc/$', views.paper4, name="paper4"),
    url(r'^scrapeie/$', views.scrapeie, name="scrapeie"),
    url(r'^ie/$', views.paper5, name="paper5"),
    url(r'^scrapeit/$', views.scrapeit, name="scrapeit"),
    url(r'^it/$', views.paper6, name="paper6"),
    url(r'^scrapendtv/$', views.scrapendtv, name="scrapendtv"),
    url(r'^ndtv/$', views.paper7, name="paper7"),
    url(r'^scrapen18/$', views.scrapen18, name="scrapen18"),
    url(r'^n18/$', views.paper8, name="paper8"),
    url(r'^scrapeoneind/$', views.scrapeoneind, name="scrapeoneind"),
    url(r'^oneind/$', views.paper9, name="paper9"),
    url(r'^scrapeotlkind/$', views.scrapeotlkind, name="scrapeotlkind"),
    url(r'^otlkind/$', views.paper10, name="paper10"),
]