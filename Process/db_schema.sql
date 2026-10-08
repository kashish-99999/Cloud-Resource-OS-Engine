CREATE TABLE processes (
    pid INT PRIMARY KEY,
    priority INT,
    burst_time INT,
    arrival_time TIMESTAMP,
    completion_time TIMESTAMP,
    progress FLOAT
);

CREATE TABLE process_log (
    log_id SERIAL PRIMARY KEY,
    pid INT,
    old_state VARCHAR(20),
    new_state VARCHAR(20),
    remaining_time INT,
    progress FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
