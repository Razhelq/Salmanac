# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import jsonfield


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
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)


class TaskHistory(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Task name"),
        help_text=_("Select a task to record"),
    )
    history = jsonfield.JSONField(
        default={},
        verbose_name=_("History"),
        help_text=_("JSON containing the tasks history")
    )

    class Meta:
        verbose_name = _('Task History')
        verbose_name_plural = _('Task Histories')

    def __unicode__(self):
        return _(f"Task History of: {self.name}")
