from django.views import static
from django.conf.urls import include,url
from django.conf import settings

from libapp import views as libapp_views

urlpatterns = [
    url(r'^Books/', libapp_views.books, name='books'),
    url(r'^Dvds/', libapp_views.dvds, name='dvds'),
    url(r'^Others/', libapp_views.others, name='others'),
    url(r'^MyItem/', libapp_views.my_item, name='myItem'),
    url(r'^About/', libapp_views.about, name='about'),
    url(r'^MyAcct/', libapp_views.my_acct, name='myAcct'),
    url(r'^Register/', libapp_views.register, name='register'),
    url(r'^Base/', libapp_views.base, name='base'),
    url(r'^Details/(\d+)', libapp_views.details, name='details'),
    url(r'^NewItem/', libapp_views.new_item, name='newItem'),
    url(r'^Suggestions/', libapp_views.suggestions, name='suggestions'),
    url(r'^SearchLib/', libapp_views.search_lib, name='searchLib'),
    url(r'^Login/', libapp_views.user_login, name='login'),
    url(r'^Logout/', libapp_views.user_logout, name='logout'),
    url(r'^DataManage/', libapp_views.data_manage, name='dataManage'),
    url(r'^DataExport/', libapp_views.data_export, name='dataExport'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns.append(url(r'^media/(?P<path>.*)$', static.serve, {
        'document_root': settings.MEDIA_ROOT}))