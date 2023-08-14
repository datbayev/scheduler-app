To install the app quickly, use following docker image:

`docker pull adatbayev/scheduler-app`

To run the app locally, use following command with port forwarding:

`docker run -p 5000:5000`

This is a simple `flask` application

It has two primary endpoints:
1) `/timers/ POST(url, hours, minutes, seconds)` - should schedule hitting given url after given amount of time
2) `/timers/<timer_id> GET` - should return amount of seconds left until the execution

Few important notes:
- Timezone related calculations are performed in UTC for standartization sake
- data of the scheduled jobs is stored in SQLite, it was chosen for simplicity and portability
- `apscheduler` library is used for timer jobs scheduling
- `requests` library is used for making http requests from the python
- `SQLAlchemy` library for `apscheduler <> sqlite` communication
- the jobs themselves are also stored in SQLite for persistence purposes
