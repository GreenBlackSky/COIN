CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    password_hash VARCHAR(500) NOT NULL
);
CREATE TABLE accounts (
    user_id INT REFERENCES users,
    id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(user_id, id)
);
CREATE TABLE categories (
    user_id INT REFERENCES users,
    account_id INT NOT NULL,
    id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(8) NOT NULL,
    PRIMARY KEY(user_id, account_id, id)
);
CREATE TABLE events (
    user_id INT REFERENCES users,
    account_id INT NOT NULL,
    id INT NOT NULL,
    category_id INT NOT NULL,
    event_time TIMESTAMP NOT NULL,
    diff INT NOT NULL,
    description VARCHAR(200) NOT NULL,
    PRIMARY KEY(user_id, account_id, id)
);
CREATE TABLE save_points (
    user_id INT REFERENCES users,
    account_id INT NOT NULL,
    id INT NOT NULL,
    datetime TIMESTAMP NOT NULL,
    total INT NOT NULL,
    PRIMARY KEY(user_id, account_id, id)
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