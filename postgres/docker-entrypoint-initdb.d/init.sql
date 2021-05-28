
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE labels (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    color VARCHAR(6)
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    account_id INT REFERENCES accounts,
    diff INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    result_balance FLOAT NOT NULL,
    confirmed BOOLEAN NOT NULL
);
CREATE TABLE events_labels (
    event_id INT REFERENCES events,
    label_id INT REFERENCES labels
);
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    account_id INT REFERENCES accounts,
    diff INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    last_confirmed TIMESTAMP NOT NULL,
    active BOOLEAN NOT NULL,
    cycle INT NOT NULL,
    cycle_length INT NOT NULL
);
CREATE TABLE templates_labels (
    template_id INT REFERENCES templates,
    label_id INT REFERENCES labels
);