# -*- coding: utf-8 -*-
from builtins import Exception

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime
from myapp.models import TaskHistory

from shpacoo_portal.views import Scheduled_Album_Finder

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")), ignore_result=True)
def find_albums_task():
    logger.info("Start task")
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
    logger.info(f'Task finished: result = {result}')






