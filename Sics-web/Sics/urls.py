"""MulVAL_BAG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from MulVAL2B.views import window, mulval, download, a2b, mulvalerror1, mulvalerror2, mulvalsuccess, a2berror
from blog.views import blog_detail, like_change, blog_list, toHome, contactsuccess, contactme, contactfail
from Grass.views import grass_main
from ToMulVAL.views import toMulVAL,tomulvalupload,tomulvaldownload
from django.views import static
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static as sta
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', toHome, name='home'),
    path('contactme/', contactme),
    path('contactsuccess/', contactsuccess),
    path('contactfail/', contactfail),
    path('blog/home/', blog_list, name="blog_list"),
    path('blog/<int:blog_pk>/', blog_detail, name="blog_detail"),
    path('blog/ckeditor/', include('ckeditor_uploader.urls')),
    path('blog/like_change/', like_change, name="like_change"),
    path('mulval/window/', window, name="mulval_window"),
    path('mulval/mulval/', mulval),
    path('mulval/download/', download),
    path('mulval/a2b/', a2b),
    path('mulval/mulvalerror1/', mulvalerror1),
    path('mulval/mulvalsuccess/', mulvalsuccess),
    path('mulval/mulvalerror2/', mulvalerror2),
    path('mulval/a2berror/', a2berror),
    path('grass/',grass_main, name="grass_main"),
    path('toMulVAL/',toMulVAL,name="toMulVAL"),
    path('ToMulVAL/tomulvalupload/',tomulvalupload),
    path('ToMulVAL/tomulvaldownload/',tomulvaldownload),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^favicon\.ico$',RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^banner\.jpg$',RedirectView.as_view(url=r'static/images/banner.jpg')),
    # url(r'^总流程详图(深色)\.png$',RedirectView.as_view(url=r'/static/images/totalprocess.png'))
]
