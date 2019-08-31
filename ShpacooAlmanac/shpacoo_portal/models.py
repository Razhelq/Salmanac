# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(
        verbose_name='Artist picture',
        upload_to='pictures/',
        null=True,
    )
    user = models.ManyToManyField(User)


class Album(models.Model):
    title = models.CharField(max_length=128)
    release_date = models.DateTimeField()
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)


class ScrappedData(models.Model):
    artist_name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    release_date = models.DateTimeField()
