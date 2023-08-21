CREATE TABLE IF NOT EXISTS timers (
    timer_id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    scheduled_on INTEGER NOT NULL -- datetime when it was scheduled
);
