from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import g

import config
import requests


def schedule_new_job(url, timer_id, time_to_call_back):
    new_job = get_scheduler().add_job(
        func=job_callback,
        trigger='date',
        args=[url, timer_id],
        id=f'job_id_{timer_id}',
        next_run_time=time_to_call_back
    )

    return new_job


def job_callback(url, timer_id):
    url_to_hit = "http://127.0.0.1:5000/timers/ping" if config.DEBUG else url

    if url[-1] != '/':
        url_to_hit += '/'

    url_to_hit += str(timer_id)

    response = requests.post(url_to_hit)
    # do something here with the response object for further processing


def get_scheduler():
    scheduler = getattr(g, '_scheduler', None)
    if scheduler is None:

        jobstore = {
            'default': SQLAlchemyJobStore(url=f'sqlite:///{config.DATABASE}')
        }

        scheduler = g._scheduler = BackgroundScheduler(
            timezone=config.TIMEZONE,
            jobstores=jobstore
        )
        scheduler.start()

    return scheduler
