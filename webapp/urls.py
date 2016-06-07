"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from libapp import views as libapp_views
from django.conf.urls import include,url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', libapp_views.index , name='index'),
    url(r'^index/', libapp_views.index, name='index'),
    url(r'^libapp/', include('libapp.libappurls', namespace = 'libapp')),
]
