## Home assignment

This is a temporary repo, which will be deleted after the assessment is complete.

### Installation

To install the app quickly, use following docker image:

`docker pull adatbayev/scheduler-app`

To run the app locally, use following command with port forwarding:

`docker run -p 5000:5000`

### Brief description

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

Prints are all over for debugging purposes on local machine during the development.

### Storage

For simplicity and portability purposes SQLite was chosen as a storage. You can find it [`db`](db) folder. Initial schema is also provided to create the table.

During the containerization something went wrong with persisting scheduled jobs themselves into the SQLite. So they're stored in memory of the app at the moment. Somehow it was working fine on my laptop, but when I tried to put everything into containers, things started to break. It's related to versions of python libraries that I'm using, something related to `apscheduler`. And using the memory as a backend for the jobs means if you restart the app, jobs themselves will be gone. Though the metadata of the jobs is stored fine in the SQLite.
