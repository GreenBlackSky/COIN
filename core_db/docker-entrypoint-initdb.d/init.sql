CREATE TABLE accounts (
    user_id INT,
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    color INT
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INT,
    account_id INT REFERENCES accounts,
    event_time TIMESTAMP NOT NULL,
    diff INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    category_id INT REFERENCES categories
);
CREATE TABLE save_points (
    id SERIAL PRIMARY KEY,
    user_id INT,
    account_id INT REFERENCES accounts,
    datetime TIMESTAMP NOT NULL,
    total FLOAT NOT NULL
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