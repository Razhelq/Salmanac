# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=128)
    picture = models.ImageField(
        verbose_name='Artist picture',
        upload_to='pictures/',
        null=True,
    )


class Album(models.Model):
    title = models.CharField(max_length=128)
    release_date = models.DateTimeField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
