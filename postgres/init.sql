CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(200) NOT NULL,
    password_hash VARCHAR(500) NOT NULL
);
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    name VARCHAR(100) NOT NULL,
    actual_date DATE NOT NULL,
);
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    color VARCHAR(6),
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    account_id INT REFERENCES accounts,
    time TIME NOT NULL,
    diff INT NOT NULL,
    category_id INT REFERENCES categories,
    description VARCHAR(200) NOT NULL,
    confirmed BOOLEAN NOT NULL
);
CREATE TABLE templates (
    id SERIAL PRIMARY KEY,
    active BOOLEAN NOT NULL,
    account_id INT REFERENCES accounts,
    time TIME NOT NULL,
    diff INT NOT NULL,
    category_id INT REFERENCES categories,
    description VARCHAR(200) NOT NULL,
    last_confirmed_date DATE NOT NULL,
    template INT NOT NULL,
    cycle_length INT NOT NULL
);
