# primary business logic that connects controllers and models, which are inserted into db
from sqlite3 import DatabaseError

from flask import g
from datetime import datetime, timedelta

import sqlite3
import config
from exceptions.record_not_found_error import RecordNotFoundError


def get_timer_by_id(timer_id):
    timer = query_db('select * from timers where timer_id = ?', [timer_id], one=True)
    if timer is None:
        raise RecordNotFoundError(timer_id)

    return timer


def insert_new_timer(url, when_to_call_back):
    new_timer_record = insert_to_db(
        'insert into timers (url, scheduled_on) values(?, (strftime(\'%s\', ?)))',
        [url, when_to_call_back]
    )

    if not new_timer_record:
        raise DatabaseError("Error during inserting new timer")

    return new_timer_record


def insert_to_db(query, args=()):
    db = get_db_instance()
    result = db.execute(query, args)
    db.commit()

    return result


def get_db_instance():
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE)

    db.row_factory = make_dicts

    return db


def query_db(query, args=(), one=False):
    cur = get_db_instance().execute(query, args)
    result = cur.fetchall()
    cur.close()

    return (result[0] if result else None) if one else result
