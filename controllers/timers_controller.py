# Primary controller that sits between Routes and Services
# Controller shouldn't go to db directly, but rather through Services
from sqlite3 import DatabaseError
import urllib3

from flask import request
from datetime import datetime, timedelta

from exceptions.record_not_found_error import RecordNotFoundError
from services import db_service, scheduling_service


def ping(ping_id):
    return {'status': 'OK', 'message': f'Ping id {ping_id} is successful!'}, 200


def set_timer():
    # Parse and validate input parameters first
    url = request.json.get('url')  # the url that we'd like to hit once the timer is over
    if not url:
        return {'error': 'URL param missing'}, 422

    url_parse_result = urllib3.util.parse_url(url)
    if not all([url_parse_result.scheme, url_parse_result.netloc]):
        return {'error': 'Invalid URL'}, 422

    try:
        hours = int(request.json.get('hours'))
        minutes = int(request.json.get('minutes'))
        seconds = int(request.json.get('seconds'))
    except ValueError as exc:
        return {'error': f'Invalid time value types, error: {exc}'}, 422
    except TypeError:
        return {'error': f'You must provide all three (hours, minutes and seconds)'}, 422

    # Translate input parameters into total seconds
    total_sec = seconds + minutes * 60 + hours * 3600
    when_to_call_back = datetime.utcnow() + timedelta(seconds=total_sec)

    # Try to insert the record into database first
    try:
        new_timer_db_record = db_service.insert_new_timer(url, when_to_call_back)
    except DatabaseError as exc:
        return {'error': str(exc)}, 500

    # Return error if something went wrong with the database
    if new_timer_db_record is None or not hasattr(new_timer_db_record, "lastrowid"):
        return "Database error", 500

    # Schedule the timer only if successfully inserted into database
    new_timer_id = new_timer_db_record.lastrowid
    try:
        new_timer_job = scheduling_service.schedule_new_job(url, new_timer_id, when_to_call_back)
    except Exception as exc:
        return f"Error on scheduling the job: {exc}", 500

    # Normal http code 200 success
    return {'id': new_timer_id,
            'time_left': total_sec}


def get_timer(timer_id):
    try:
        timer = db_service.get_timer_by_id(timer_id)
        scheduled_on = datetime.utcfromtimestamp(timer["scheduled_on"])
        utc_now = datetime.utcnow()

        # If the timer is still "in the future"
        if utc_now < scheduled_on:
            diff_time = scheduled_on - utc_now
            diff_time_sec = diff_time.seconds

            result = {
                'id': timer_id,
                'time_left': diff_time_sec
            }
        # Timer is in the past
        else:
            result = {
                'id': timer_id,
                'error': "Timer expired already"
            }

        return result  # normal http 200 success
    except RecordNotFoundError as exc:
        return {'error': str(exc)}, 404
    except DatabaseError as exc:
        return {'error': str(exc)}, 500
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}, 500
