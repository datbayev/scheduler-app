## Home assignment

This is a temporary repo, which will be deleted after the assessment is complete.

### Brief description

This is a simple `flask` application

It has two primary endpoints:
1) `/timers/ POST(url, hours, minutes, seconds)` - should schedule hitting given url after given amount of time
2) `/timers/<timer_id> GET` - should return amount of seconds left until the execution

Few important notes:

- application is following MVC pattern as you can see the code is split into dedicated entities like [controller layer](controllers/timers_controller.py), [service layer](services) and [route layer](routes/blueprint.py)
- input is validated on the controller layer and only valid data is passed through to the service layer
- exceptions are caught as much as it's possible on controller layer for better error handling and more descriptive error for users
- configurations are stored in [config.py](config.py) file
- there's an `/timers/ping/<ping_id>` endpoint for testing purposes to validate that scheduled jobs indeed do hit the url
- Timezone related calculations are performed in UTC for standartization sake
- data of the scheduled jobs is stored in SQLite, it was chosen for simplicity and portability
- `apscheduler` library is used for timer jobs scheduling
- `requests` library is used for making http requests from the python
- `SQLAlchemy` library for `apscheduler <> sqlite` communication
- the jobs themselves are also stored in SQLite for persistence purposes

### Storage

For simplicity and portability purposes SQLite was chosen as a storage. You can find it [`db`](db) folder. Initial schema is also provided to create the table.


### Containers

For velocity purposes it was decided to drop the containerization as there were python libraries version compatibility issues.

### Further work

There is a bit of room for further improvement:
1) containerization
2) ORM

First one would ensure portability and easy installation, second one would enhance flexibility and easier code maintenance with database related business logic
