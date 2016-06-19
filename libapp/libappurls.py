from django.conf.urls import url
from django.contrib import admin
from libapp import views as libapp_views

urlpatterns = [
    url(r'^books/', libapp_views.books, name='books'),
    url(r'^dvds/', libapp_views.dvds, name='dvds'),
    url(r'^others/', libapp_views.others, name='others'),
    url(r'^about/', libapp_views.about, name='about'),
    url(r'^myacct/', libapp_views.my_acct, name='myacct'),
    url(r'^register/', libapp_views.register, name='register'),
    url(r'^base/', libapp_views.base, name='base'),
    url(r'^details/(\d+)', libapp_views.details, name='details'),
    url(r'^newitem/', libapp_views.newitem, name='newitem'),
    url(r'^suggestions/', libapp_views.suggestions, name='suggestions'),
    url(r'^searchlib/', libapp_views.searchlib, name='searchlib'),
    url(r'^searchresult/', libapp_views.searchresult, name='searchresult'),
]