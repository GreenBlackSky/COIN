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
    actual_date DATE,
    balance INT,
    unconfirmed_balance INT
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
    description VARCHAR(200)
);
CREATE TABLE events (
    date DATE,
    time TIME,
    diff INT,
    category_id INT REFERENCES categories,
    description VARCHAR(200),
    account_id INT REFERENCES accounts,
    confirmed BOOLEAN
);
CREATE TABLE templates (
    start_date DATE,
    time TIME,
    diff INT,
    category_id INT REFERENCES categories,
    description VARCHAR(200),
    account_id INT REFERENCES accounts,
    template VARCHAR(50)
);
