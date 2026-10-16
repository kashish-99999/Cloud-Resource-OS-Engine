CREATE TABLE process_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pid INT,
    old_state TEXT,
    new_state TEXT,
    enter_time TEXT,
    leave_time TEXT,
    completion_percent INT
);
