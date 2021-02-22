CREATE TABLE test_data (
    id SERIAL PRIMARY KEY,
    value text
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(200)  NOT NULL
);
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users
);
CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    is_actual BOOLEAN NOT NULL DEFAULT false,
    date DATE NOT NULL,
    balance INT NOT NULL,
    unconfirmed_balance INT
);
CREATE UNIQUE INDEX only_one_current_balance 
   ON dates (account_id)
   WHERE is_actual;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    hidden BOOLEAN
);
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    date_id INT REFERENCES dates,
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
    last_confirmed_date INT REFERENCES dates,
    template INT NOT NULL,
    cycle_length INT NOT NULL
);
