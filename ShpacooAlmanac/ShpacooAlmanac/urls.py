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

from shpacoo_portal.views import TestView, UserCreateView, LoginView, AddArtistView, FindAlbumView, DisplayAlbumsView, \
    IndexView, DeleteArtistView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^test/$', TestView.as_view(), name='test'),
    url(r'^$', UserCreateView.as_view(), name='user-create'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^add_artist/$', AddArtistView.as_view(), name='add-artist'),
    url(r'^find_album/(?P<id>(\d)*)/$', FindAlbumView.as_view(), name='find-album'),
    url(r'^display_album/', DisplayAlbumsView.as_view(), name='display-albums'),
    url(r'^delete_artist/(?P<id>(\d)*)/$', DeleteArtistView.as_view(), name='delete-artist'),
]
