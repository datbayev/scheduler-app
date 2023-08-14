from datetime import datetime, timedelta
import os
import requests
import sqlite3

from flask import Flask, request, g
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'db', 'sqlite.db')


def get_db():
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = make_dicts

    return db


def get_scheduler():
    scheduler = getattr(g, '_scheduler', None)
    if scheduler is None:

        # below is the configuration for storing scheduled jobs
        # persistence of jobs in SQLite worked fine on my local machine
        # but something is messed up with the library versions
        # so with following lines being commented out means jobs are stored in memory and are not persisted

        # jobstore = {
        #     'default': SQLAlchemyJobStore(url=f'sqlite:///{DATABASE}')
        # }

        scheduler = g._scheduler = BackgroundScheduler(
            timezone='utc'
            # jobstores=jobstore
        )
        scheduler.start()

    return scheduler


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    return (rv[0] if rv else None) if one else rv


def insert_to_db(query, args=()):
    db = get_db()
    result = db.execute(query, args)
    db.commit()
    return result


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index_page():
    return "Index page"


@app.route('/timers/', methods=['POST'])
def set_timer():
    url = request.form.get('url')  # the url that we'd like to hit once the timer is over

    hours = int(request.form.get('hours'))
    minutes = int(request.form.get('minutes'))
    seconds = int(request.form.get('seconds'))

    total_sec = seconds + minutes * 60 + hours * 3600  # translate into total seconds
    when_to_call_back = datetime.utcnow() + timedelta(seconds=total_sec)

    new_timer = insert_to_db(
        'insert into timers (seconds, url, scheduled_on) values(?, ?, (strftime(\'%s\', ?)))',
        [total_sec, url, when_to_call_back]
    )

    new_timer_id = new_timer.lastrowid

    get_scheduler().add_job(
        func=job_callback,
        trigger='date',
        args=[url, new_timer_id],
        id=f'job_id_{new_timer_id}',
        next_run_time=when_to_call_back
    )

    result = {
        'id':new_timer_id,
        'time_left':total_sec
    }

    return result


def job_callback(url, timer_id):
    # print(f'Calling back url {url}, the timer id is {timer_id}')

    url_to_hit = url

    if url[-1] != '/':
        url_to_hit += '/'

    url_to_hit += str(timer_id)

    # print("making request...")
    response = requests.post(url_to_hit)
    # do something here with the response object
    # print("request finished!")
    # print(response.status_code)


@app.route('/timers/<int:timer_id>', methods=['GET'])
def get_timer(timer_id):
    # print(f'Getting the timer with id={timer_id}')
    timer = query_db('select * from timers where timer_id = ?', [timer_id], one=True)
    if timer is None:
        result = f'No such timer found'
        # print(f'No timer with id={timer_id} was found')
    else:
        scheduled_on = datetime.utcfromtimestamp(timer["scheduled_on"])
        utc_now = datetime.utcnow()
        if utc_now < scheduled_on:
            diff_time = scheduled_on - utc_now
            diff_time_sec = diff_time.seconds
            # print(f"utc_now={utc_now}, "
            #       f"scheduled_on = {scheduled_on}, "
            #       f"diff_time = {diff_time}"
            #       f"diff_time_sec = {diff_time_sec}"
            #       )
            result = {
                'id': timer_id,
                'time_left': diff_time_sec
            }
        else:
            result = {
                'id': timer_id,
                'error': "Timer expired already"
            }
            # print(f"Time is already in the past for this timer...")

    return result
