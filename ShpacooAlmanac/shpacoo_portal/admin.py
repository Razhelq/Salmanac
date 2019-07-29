# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Artist, Album


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'picture']


@admin.register(Album)
class AlbumModel(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'artist']
