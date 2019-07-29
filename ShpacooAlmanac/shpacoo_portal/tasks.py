# -*- coding: utf-8 -*-
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

    Scheduled_Album_Finder.get()


    
