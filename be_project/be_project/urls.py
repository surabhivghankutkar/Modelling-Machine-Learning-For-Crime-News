from django.contrib import admin
from django.conf.urls import url, include
from django.contrib import admin
#from crime_analysis import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('crime_analysis.urls')),
]

urlpatterns += staticfiles_urlpatterns()