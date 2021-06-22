CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE events (
    user_id INT,
    account_id INT REFERENCES accounts,
    id SERIAL PRIMARY KEY,
    event_time TIMESTAMP NOT NULL,
    diff INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    confirmed BOOLEAN NOT NULL
);
CREATE TABLE save_points (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    total FLOAT NOT NULL
)
CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    color VARCHAR(6)
);
CREATE TABLE events_labels (
    event_id INT REFERENCES events,
    label_id INT REFERENCES labels
);
CREATE TABLE accounts_labels (
    account_id INT REFERENCES accounts,
    label_id INT REFERENCES labels
);
-- CREATE TABLE templates (
--     id SERIAL PRIMARY KEY,
--     time TIMESTAMP NOT NULL,
--     account_id INT REFERENCES accounts,
--     diff INT NOT NULL,
--     description VARCHAR(200) NOT NULL,
--     last_confirmed TIMESTAMP NOT NULL,
--     active BOOLEAN NOT NULL,
--     cycle INT NOT NULL,
--     cycle_length INT NOT NULL
-- );
-- CREATE TABLE templates_labels (
--     template_id INT REFERENCES templates,
--     label_id INT REFERENCES labels
-- );