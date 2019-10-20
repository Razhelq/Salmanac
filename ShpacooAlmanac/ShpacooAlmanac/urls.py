"""ShpacooAlmanac URL Configuration

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

from shpacoo_portal.views import TestView, LoginRegisterView, AddArtistView, DisplayAlbumsView, \
    IndexView, DeleteArtistView, FindAlbumsView, LogoutView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^login_register/$', LoginRegisterView.as_view(), name='login-register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^add_artist/$', AddArtistView.as_view(), name='add-artist'),
    url(r'^display_album/$', DisplayAlbumsView.as_view(), name='display-albums'),
    url(r'^delete_artist/(?P<id>(\d)*)/$', DeleteArtistView.as_view(), name='delete-artist'),
    url(r'^find_albums/$', FindAlbumsView.as_view(), name='find-albums')
]
