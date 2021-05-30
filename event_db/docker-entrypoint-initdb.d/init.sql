CREATE TABLE events (
    user_id INT,
    account_id INT,
    id SERIAL PRIMARY KEY,
    event_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    diff INT NOT NULL,
    total FLOAT NOT NULL,
    description VARCHAR(200) NOT NULL,
    confirmed BOOLEAN NOT NULL
);
CREATE TABLE events_labels (
    event_id INT REFERENCES events,
    label_id INT
);