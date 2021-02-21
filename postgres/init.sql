CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    value text
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    password_hash VARCHAR(200)
);
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    actual_date DATE
);
CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    date DATE,
    balance INT,
    unconfirmed_balance INT
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    name VARCHAR(100),
    description VARCHAR(200),
    hidden BOOLEAN
);
CREATE TABLE events (
    date_id DATE INT REFERENCES dates,
    account_id INT REFERENCES accounts,
    time TIME,
    diff INT,
    category_id INT REFERENCES categories,
    description VARCHAR(200),
    confirmed BOOLEAN
);
CREATE TABLE templates (
    active BOOLEAN,
    account_id INT REFERENCES accounts,
    time TIME,
    diff INT,
    category_id INT REFERENCES categories,
    description VARCHAR(200),
    last_confirmed_date DATE,
    template INT,
    cycle_length INT
);
