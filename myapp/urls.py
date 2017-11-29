"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from HPAdmin.views import *
from HomePage.views import *
from kindeditor.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^index$', index),
    url(r'^information$', information),
    url(r'^case$', case),
    url(r'^about$', about),

    url(r'^news/(\d*)', news),
    url(r'^uptest$', uptest),
    url(r'^testviews$', testviews),
    url(r'^kindeditor/uploads/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),

    url(r'^admins$', adminlogin),
    url(r'^admins/manage$', adminmanage),
    url(r'^admins/logout$', adminlogout),
    url(r'^admins/banner/(\d*)', adminbanner),
    url(r'^admins/movie/(\d*)', adminmovie),
    url(r'^admins/bullhorn/(\d*)', adminbullhorn),
    url(r'^admins/case/(\d*)', admincase),
    url(r'^admins/news/(\d*)', adminnews),
    url(r'^validate/$', validate, name='validate'),
    url(r'^admins/usermanage/(\d*)$', adminusermanage),
    url(r'^admins/domanage/(\d*)$', admindomanage),
    url(r'^admins/menumanage$', adminmenumanage),
    url(r'^admins/operationlog/(\d*)$', adminoperationlog),
    url(r'^admins/message/(\d*)$', adminmessage),
    url(r'^admins/chartdata$', adminchartdata),
    url(r'^admins/chartdatas$', adminchartdatas),
]
