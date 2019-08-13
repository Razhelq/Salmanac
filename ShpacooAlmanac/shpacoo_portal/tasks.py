# # Create your tasks here
# from __future__ import absolute_import, unicode_literals
# from celery import shared_task
#
#
# @shared_task
# def add(x, y):
#     return x + y
#
#
# @shared_task
# def mul(x, y):
#     return x * y
#
#
# @shared_task
# def xsum(numbers):
#     return sum(numbers)
#
#

# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from builtins import Exception

from datetime import datetime

import celery

from shpacoo_portal.models import TaskHistory
from shpacoo_portal.views import Scheduled_Album_Finder

@celery.task
def find_albums_task():
    # logger.info("Start task")
    now = datetime.now()
    date_now = now.strftime("%d-%m-%Y %H:%M:%S")
    name = 'Album finder task'
    try:
        Scheduled_Album_Finder.get()
        result = 'Task completed successfully'
    except Exception as e:
        result = f'Error occured - {e}'
    task_history = TaskHistory.objects.get_or_create(name=name)[0]
    task_history.history.update({date_now: result})
    task_history.save()
    # logger.info(f'Task finished: result = {result}')






